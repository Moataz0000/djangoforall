from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from .models import Post, Subscription
from django.conf import settings

@receiver(post_save, sender=Post)
def send_post_notification(sender, instance, created, **kwargs):
    if created and instance.active:  
        subscribers = Subscription.objects.values_list('email', flat=True)

        post_url = f"{settings.BASE_URL}{reverse('blog:post_detail', args=[instance.slug])}"

        subject = f'منشور جديد: {instance.title}'

        content_preview = instance.content[:100] + '...' if len(instance.content) > 100 else instance.content

        # رسالة نصية بسيطة
        plain_message = (
            f'تحقق من منشوري الجديد:\n\n'
            f'العنوان: {instance.title}\n'
            f'المحتوى: {content_preview}\n'
            f'اقرأ المزيد: {post_url}'
        )

        # إنشاء رسالة HTML محسنة
        html_message = f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f7f9fc;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 5px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    margin: 20px auto;
                }}
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                }}
                h2 {{
                    color: #2980b9;
                    margin: 10px 0;
                }}
                p {{
                    line-height: 1.6;
                    color: #34495e;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 12px;
                    color: #aaaaaa;
                    text-align: center;
                }}
                .preview {{
                    font-style: italic;
                    color: #7f8c8d;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>منشور جديد | Django For All!</h1>
                <h2>{instance.title}</h2>
                <p>إحنا متحمسين نشارك معاكم أحدث منشور في المدونة!</p>
                <p class="preview">{content_preview}</p>  <!-- Removed quotes here -->
                <p>انقر على الزر أدناه لقراءة المقالة بالكامل:</p>
                <p>
                    <a href="{post_url}" style="display: inline-block; padding: 12px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; text-align: center; transition: background-color 0.3s; margin-top: 15px;">اقرأ المزيد</a>
                </p>
            </div>
            <div class="footer">
                <p>شكراً إنك مشترك في المدونة بتاعتنا!</p>
            </div>
        </body>
        </html>
        '''

        # إرسال البريد الإلكتروني إلى كل مشترك
        for subscriber_email in subscribers:
            email = EmailMultiAlternatives(
                subject,
                plain_message,  # هذه النسخة النصية البسيطة
                settings.DEFAULT_FROM_EMAIL,
                [subscriber_email]
            )
            email.attach_alternative(html_message, "text/html")  # إرفاق محتوى HTML
            email.send()
