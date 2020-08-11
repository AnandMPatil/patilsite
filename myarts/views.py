from myarts.models import Article, Comment, Fav
from myarts.forms import CreateForm,CommentForm
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.core.files.uploadedfile import InMemoryUploadedFile
from myarts.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from myarts.utils import dump_queries
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime

class ArticleListView(OwnerListView):
    model = Article
    # By convention:
    template_name = "myarts/article_list.html"
    def get(self, request) :
        #article_list = Article.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_things.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        #ctx = {'article_list' : article_list, }
        #return render(request, self.template_name, ctx)

    #def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Article.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            query = Q(title__contains=strval)
            query.add(Q(text__contains=strval), Q.OR)
            objects = Article.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :
            # try both versions with > 4 posts and watch the queries that happen
            objects = Article.objects.all().order_by('-updated_at')[:10]
            # objects = Article.objects.select_related().all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {'article_list' : objects, 'search': strval,'favorites': favorites}
        retval = render(request, self.template_name, ctx)

        dump_queries()
        return retval;

class ArticleDetailView(OwnerDetailView):
    model = Article
    template_name = "myarts/article_detail.html"
    def get(self, request, pk) :
        x = Article.objects.get(id=pk)
        comments = Comment.objects.filter(article=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'article' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class ArticleCreateView(LoginRequiredMixin, View):
    template_name = 'myarts/article_form.html'
    success_url = reverse_lazy('myarts:all')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)

class ArticleUpdateView(LoginRequiredMixin, View):
    template_name = 'myarts/article_form.html'
    success_url = reverse_lazy('myarts:all')
    def get(self, request, pk) :
        pic = get_object_or_404(Article, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(Article, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)

class ArticleDeleteView(OwnerDeleteView):
    model = Article

def stream_file(request, pk) :
    pic = get_object_or_404(Article, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Article, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, article=f)
        comment.save()
        return redirect(reverse('myarts:article_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "myarts/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        article = self.object.article
        return reverse('myarts:article_detail', args=[article.id])


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Article, id=pk)
        fav = Fav(user=request.user, article=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Article, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, article=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()