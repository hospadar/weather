from cache import Cache
import json

base_doc =\
'''<!DOCTYPE html>
<head>
    <script type="text/javascript" src="./jquery.js"></script>
    <script type="text/javascript" src="./jquery.flot.js"></script>
    <script type="text/javascript" src="./jquery.flot.time.js"></script>
    <script type="text/javascript" src="./jquery.flot.threshold.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            data=[{
                    label:"temperatures",
                    data:%s,
                    threshold:[{
                        below:32,
                        color:"rgb(0, 0, 255)"
                    },
                    {
                        below:45,
                        color:"rgb(0, 255, 0)"
                    }],
                    color:"rgb(255, 0, 0)"
                }];
            options={
                xaxis:{
                    mode:"time",
                    timeformat: "%s",
                    twelveHourClock: true,
                    minTickSize: [4, "hour"]
                },
                grid:{
                    markings: function(axes){
                        var markings = []
                        var d = new Date(axes.xaxis.min);
                        if (d.getUTCHours() < 8){
                            var start = d.getTime()
                            d.setUTCHours(8)
                            var end = d.getTime()
                            markings.push({xaxis:{from:start, to:end}})
                        }
                        d.setUTCHours(16)
                        i = d.getTime()
                        do{
                            if (i+12*60*60*1000 < axes.xaxis.max){
                                markings.push({xaxis:{from: i, to: i+12*60*60*1000}})
                            }else{
                                markings.push({xaxis:{from: i}})
                            }
                            i = i+24*60*60*1000
                        }while(i<axes.xaxis.max)
                        return markings
                    }
                },
                
            };
            p = $.plot($('div#placeholder')[0], data, options);
        });
    </script>
</head>
<body>
    <div id="placeholder" style="border:1px solid #000;width:1200px;height:600px"></div>
</body>
'''

if __name__ == '__main__':
    output = open("chart.html", "w")
    cache = Cache('temps.db')
    cache.connect()
    cache.cursor.execute("select * from cache order by key")
    data = []
    for ziptime, temp in cache.cursor:
        zip, time = ziptime.split('_')
        data.append([float(time)*1000 - (5*60*60*1000), temp])
        
    output.write(base_doc % (json.dumps(data), "%y-%m-%d"))