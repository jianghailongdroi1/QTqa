def process(request, **kwargs):
    app = kwargs.pop('app', None)
    index = kwargs.pop('index',None)
    fun = kwargs.pop('function', None)

    if index == "1":
        try:
            appObj = __import__("%s.views_suite" % app)
            viewObj = getattr(appObj, 'views_suite')
            funcObj = getattr(viewObj, fun)
        # 执行view.py中的函数，并获取其返回值
            result = funcObj(request)
        except (ImportError, AttributeError):
             raise
    if (index=="2"):
        try:
            appObj = __import__("%s.views_jiajia" % app)
            viewObj = getattr(appObj, 'views_jiajia')
            funcObj = getattr(viewObj, fun)

            # 执行view.py中的函数，并获取其返回值
            result = funcObj(request)
            print(result)
        except (ImportError, AttributeError):
            raise
    if (index=="3"):
        try:
            appObj = __import__("%s.views_project" % app)
            viewObj = getattr(appObj, 'views_project')
            funcObj = getattr(viewObj, fun)

            # 执行view.py中的函数，并获取其返回值
            result = funcObj(request)
            print(result)
        except (ImportError, AttributeError):
            raise

    if (index=="4"):
        try:
            appObj = __import__("%s.views_job_result" % app)
            viewObj = getattr(appObj, 'views_job_result')
            funcObj = getattr(viewObj, fun)

            # 执行view.py中的函数，并获取其返回值
            result = funcObj(request)
        except (ImportError, AttributeError):
            raise

    elif (index == "5"):
        try:
            appObj = __import__("%s.views_job" % app)
            viewObj = getattr(appObj, 'views_job')
            funcObj = getattr(viewObj, fun)

            # 执行view.py中的函数，并获取其返回值
            result = funcObj(request)
        except (ImportError, AttributeError):
            raise
    return result



