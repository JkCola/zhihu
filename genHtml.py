# coding: utf-8

htmlTpl = '''
<!DOCTYPE html>
<html lang="zh-cn">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Zhihu Daily</title>
        <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css">
        <!--[if lt IE 9]>
          <script src="http://cdn.bootcss.com/html5shiv/3.7.2/html5shiv.min.js"></script>
          <script src="http://cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
        <![endif]-->
        <style type="text/css">
*, body {
    font-family: Consolas, Microsoft Yahei;
}
.day_stories {
    box-shadow: 1px 1px 10px 4px #f0f0f0;
    padding: 10px 70px;
    clear: both;
}
.day_stories .story_date {
    font-size: 20px;
    width: inherit;
    font-weight: bold;
}
.day_stories .story_url {
    width: inherit;
    height: 50px;
    margin: 2px 0px;
    color: #4B5CC4;
    font-weight: bold;
    font-size: 10px;
}
.day_stories .story_url:hover {
    text-shadow: 0px 0px 10px #EF7A82;
}
.day_stories .story_url span {}
.day_stories .story_url img {
    height: 50px;
    width: 50px;
    margin-right: 20px;
}
        </style>
    </head>
    <body>
        <div class="container">
            {{day_stories_body}}
        </div>
    </body>
</html>
<script src="http://cdn.bootcss.com/jquery/1.11.1/jquery.min.js"></script>
<script src="http://cdn.bootcss.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>
<script type="text/javascript">
    console.log('Email: jk.wong@qq.com');
</script>
'''
dayStoriesTpl = '''
<div class="row day_stories"><div class="col-md-12">
    <div class="story_date">
        <span>{{day_stories_title}}</span>
    </div>
    {{story_url_body}}
</div></div>
'''
storyUrlTpl = '''
<div class="story_url">
    <a href="{{story_url}}" target="_blank">
        <img src="{{story_img_src}}" alt="">
        <span>{{story_title}}</span>
    </a>
</div>
'''
def do(stories):
    storyGroupByDate = {}
    for row in stories:
        story = {
            'id': row[0],
            'url': row[1],
            'title': row[2],
            'imgSrc': row[3],
            'create_time': row[4]
        }
        ymd = story['create_time'].strftime('%Y-%m-%d')
        if ymd not in storyGroupByDate:
            storyGroupByDate[ymd] = []
        storyGroupByDate[ymd].append(story)

    dayStoriesList = []
    for ymd in storyGroupByDate:
        storyUrlList = []
        for story in storyGroupByDate[ymd]:
            htmlStr = storyUrlTpl.replace('{{story_img_src}}', story['imgSrc'])\
                        .replace('{{story_url}}', story['url'])\
                        .replace('{{story_title}}', story['title'])
            storyUrlList.append(htmlStr)
        htmlStr = dayStoriesTpl.replace('{{day_stories_title}}', ymd)\
                    .replace('{{story_url_body}}', ''.join(storyUrlList))
        dayStoriesList.append(htmlStr)
    fileObj = open('zhihu.html', 'w')
    fileObj.write( htmlTpl.replace('{{day_stories_body}}', ''.join(dayStoriesList)) )
    fileObj.close()

if __name__ == '__main__':
    do([])
