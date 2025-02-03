from django.db import models

# Add these:
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render

from django.contrib.auth.models import User


from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtailseo.models import SeoMixin, SeoType, TwitterCard
from wagtail.images.models import Image
from wagtail.images.models import AbstractImage
from typing import Optional
from datetime import datetime
from wagtailseo.models import SeoMixin

# from wagtail.admin.panels import MultiFieldPanel
# from wagtail.images.panels import ImageChooserPanel


class ArticlePage(SeoMixin, Page):
    ...

    # Indicate this is article-style content.
    seo_content_type = SeoType.ARTICLE

    # Change the Twitter card style.
    seo_twitter_card = TwitterCard.LARGE

    promote_panels = SeoMixin.seo_panels


# class BlogIndexPage(Page):
#     intro = RichTextField(blank=True)
#     body = RichTextField(blank=True)

#     content_panels = Page.content_panels + [
#         FieldPanel('intro'),FieldPanel('body')
#     ]

class BlogIndexPage(Page):
    template = "blog/blog_index_page.html"
    intro = RichTextField(blank=True)
    body =  RichTextField(blank=True)

    # Add the main_image method:
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('intro'),FieldPanel('body'),

        InlinePanel('gallery_images', label="Gallery images"),
    ]
    
    # def serve(self, request):
    #     context = self.get_context(request)

    #     if request.method == "POST":
    #         form = CommentForm(request.POST)
    #         if form.is_valid():
    #             comment = form.save(commit=False)
    #             comment.blog = self
    #             comment.save()
    #             return redirect(self.url)  # Refresh page after submitting a comment
    #     else:
    #         form = CommentForm()

    #     context['form'] = form
    #     return render(request, 'blog/blog_index_page.html', context)

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogPage.objects.live().public().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 6)  # Ensure the second argument is 2
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts
        # context["categories"] = BlogCategory.objects.all()
        # print(context)
        return context
 

# from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtailseo.models import SeoMixin, SeoType, TwitterCard
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from django.db import models
from typing import Optional


class BlogPage(SeoMixin, Page):
    # Indicate this is article-style content.
    seo_content_type = SeoType.ARTICLE

    # Change the Twitter card style.
    seo_twitter_card = TwitterCard.LARGE

    date = models.DateField("Post date")
    intro = models.CharField(max_length=4000)
    body = RichTextField(blank=True)
    

    # SEO Fields
    custom_seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True)
    seo_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    seo_author = models.CharField(max_length=255, blank=True)

    # Gallery
    # add_gallery_images = models.ManyToManyField('wagtailimages.Image', blank=True, related_name='blog_page_gallery')
    blog_image = models.ForeignKey(
        Image,
        # on_delete=models.CASCADE,  # Specify on_delete behavior
        on_delete=models.SET_NULL,
        blank=True,  # Allow this field to be blank if necessary
        null=True,   # Allow this field to be null if necessary
    )


    # SEO Panels (for admin interface)
    promote_panels = SeoMixin.seo_panels

    # Override the seo_description method
    @property
    def seo_description(self) -> str:
        """Provide the SEO description for the page"""
        return self.intro[:160] if self.intro else "Default description"

    @property
    def seo_pagetitle(self) -> str:
        """Provide the SEO page title for the page"""
        return self.custom_seo_title if self.custom_seo_title else self.title

    @property
    def get_seo_image(self) -> Optional[Image]:
        """Get the image for the Open Graph SEO"""
        if hasattr(self, 'seo_image') and self.seo_image:
            return self.seo_image
        return self.main_image()

    def main_image(self):
        """Return the main image (first image in gallery or blog image)"""
        gallery_item = self.add_gallery_images.first()
        if gallery_item:
            return gallery_item.image
        return None
    # def main_image(self):
    #     return self.add_gallery_images.first() or None

    # Search fields for SEO
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('custom_seo_title'),  # Use custom_seo_title instead of seo_title
        # FieldPanel('seo_description'),
        # FieldPanel('seo_image'),
        # FieldPanel('add_gallery_images'),
        InlinePanel('add_gallery_images', label="Gallery images"),
        FieldPanel('seo_author'),
    ]

    # like_counts = models.PositiveIntegerField(default=0)  # Field to store the like count

# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     blog = models.ForeignKey(BlogPage, on_delete=models.CASCADE)
#     liked_on = models.DateTimeField(auto_now_add=True)

# class Meta:
#     unique_together = ('user', 'blog')

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogIndexPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=50)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

class BlogPageGalleryImage_blog(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='add_gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=50)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]





      


# from django.db import models
# from django.shortcuts import redirect
# from wagtail.models import Page
# from wagtail.fields import RichTextField
# from wagtail.admin.panels import FieldPanel
# from wagtail.documents.models import Document
# from wagtail.images.models import Image

# class FileManagementPage(Page):
#     template = 'file_management_page.html'

#     description = RichTextField(blank=True)

#     content_panels = Page.content_panels + [
#         FieldPanel('description'),
#         InlinePanel('file_links', label="Files"),
#         InlinePanel('image_links', label="Images"),
#     ]

#     def serve(self, request):
#         if request.method == 'POST':
#             file = request.FILES.get('file')
#             if file:
#                 document = Document(
#                     title=file.name,
#                     file=file,
#                 )
#                 document.save()
#                 FileLink.objects.create(page=self, document=document)

#             uploaded_image = request.FILES.get('image')
#             if uploaded_image:
#                 image = Image(
#                     title=uploaded_image.name,
#                     file=uploaded_image
#                 )
#                 image.save()
#                 ImageLink.objects.create(page=self, image=image)

#             return redirect(self.url)
        
#         return super().serve(request)

# class FileLink(models.Model):
#     page = ParentalKey(FileManagementPage, related_name='file_links')
#     document = models.ForeignKey(Document, on_delete=models.CASCADE)
#     description = RichTextField(
#         blank=True,max_length=250,
#         features=["bold", "italic", "ol", "document-link"]
#     )
#     panels = [
#         FieldPanel('document'),
#         FieldPanel('description'),
#     ]


# class ImageLink(models.Model):
#     page = ParentalKey(FileManagementPage, related_name='image_links')
#     image = models.ForeignKey(Image, on_delete=models.CASCADE)
#     description = RichTextField(
#         blank=True, max_length=250,
#         features=["bold", "italic", "ol", "document-link"]
#     )

#     panels = [
#         FieldPanel('image'),
#         FieldPanel('description'),
#     ]
