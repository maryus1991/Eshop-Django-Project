from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Blog, Blog_Category


# Create your views here.


class BlogListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    template_name = 'Eshop_Blog/blog.html'
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.filter(is_active=True, is_delete=False).order_by('-id').all()


class BlogListView_by_category(ListView):
    model = Blog
    context_object_name = 'blogs'
    template_name = 'Eshop_Blog/blog.html'
    paginate_by = 5

    def get_queryset(self):
        query = super().get_queryset()
        slug = self.kwargs.get('slug')
        return Blog.objects.filter(is_active=True, is_delete=False,
                                   select_categories__url_title__iexact=slug,
                                   select_categories__is_active=True,
                                   select_categories__is_delete=False
                                   ).order_by('-id').all()


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'Eshop_Blog/blog-single.html'

    def get_queryset(self):
        query = super(BlogDetailView, self).get_queryset()
        slug = self.kwargs.get('slug')
        query = query.filter(is_active=True, is_delete=False, slug=slug)
        return query


def Blog_Category_Partial(request):
    blog_category = Blog_Category.objects.filter(is_active=True, is_delete=False, parent_id=None)
    context = {'blog_category': blog_category}
    return render(request, 'Eshop_Blog/partial_view/Blog_Category_Partial.html', context)
