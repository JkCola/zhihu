# coding: utf-8

htmlStr = '''
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
    padding: 10px 100px;
}
.day_stories .story_date {
    font-size: 20px;
    width: inherit;

}
.day_stories .story_url {
    
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
def do(stories):
    storyGroupByDate = {}
    for row in stories:
        story = {
            'id': row[0],
            'url': row[1],
            'title': row[2],
            'create_time': row[3]
        }
        ymd = story['create_time'].strftime('%Y-%m-%d')
        if ymd not in storyGroupByDate:
            storyGroupByDate[ymd] = []
        storyGroupByDate[ymd].append(story)

    htmlList = []
    for ymd in storyGroupByDate:
        htmlList.append('''
            <div class="row day_stories"><div class="col-md-12">
                <div class="story_date">
                    <span>
            ''')
        htmlList.append(ymd)
        htmlList.append('''
                    </span>
                </div>
            ''')
        for story in storyGroupByDate[ymd]:
            htmlList.append('''
                <div class="story_url">
                    <a href="
                ''')
            htmlList.append(story['url'])
            htmlList.append('''">''')
            htmlList.append(story['title'])
            htmlList.append('''
                    </a>
                </div>
                ''')
        htmlList.append('''
            </div></div>
            ''')
    # print ''.join(htmlList)
    fileObj = open('zhihu.html', 'w')
    fileObj.write( htmlStr.replace('{{day_stories_body}}', ''.join(htmlList)) )
    fileObj.close()

if __name__ == '__main__':
    do([])
