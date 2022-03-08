# @Time: 2022/3/3 4:29 下午
# @Author: Bruce
# @Description : celery的工具模型


from flask_mail import Message
from exts import mail
from celery import Celery


# 定义任务函数
def send_mail(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient], body=body)
    try:
        mail.send(message)
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail"}


# 创建celery对象
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    taskBase = celery.Task

    class ContextTask(taskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return taskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    app.celery = celery

    # 添加任务
    celery.task(name='send_mail')(send_mail)

    return celery

