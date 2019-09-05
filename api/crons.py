from .models import Post


def test_cron_job():
    Post.objects.create(title='Cron Test Title', text="Cron Test Text", writer_id_id=1)
    pass

