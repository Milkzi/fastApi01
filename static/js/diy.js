    let text_cities = $("#text_value").val()
    let cities = JSON.parse(text_cities)

        function createProvince(){


        //console.log(text_cities)
        let cities = JSON.parse(text_cities)
        let form_province = document.getElementById('form_province');
        let form_province2 = document.getElementById('form_province2');
        for (let i=0;i<cities.length;i++){

            let now_province = cities[i]
            //console.log(now_province['provinceName'])
            form_province.options.add(new Option(now_province['provinceName'],now_province['provinceCode']))
            form_province2.options.add(new Option(now_province['provinceName'],now_province['provinceCode']))

        }
    }
    let get_cities = null;
    $('#form_province').change(function (){
        let province = $('#form_province').val();
        $("#form_city").empty();

        $("#form_area").empty();
        get_cities=null
        //console.log(province)
        let form_city = document.getElementById('form_city');

        for (let i=0;i<cities.length;i++){
            if(cities[i]['provinceCode']===province){
                get_cities = cities[i]['cities']
            }
        }
        //console.log(get_cities)
        form_city.options.add(new Option('市',''))
        for (let i=0;i<get_cities.length;i++){

            let now_city = get_cities[i]
            //console.log(now_city['cityName'])
            form_city.options.add(new Option(now_city['cityName'],now_city['cityCode']))

        }

    });

        $('#form_city').change(function (){
        let city = $('#form_city').val();
        $("#form_area").empty();

        let form_area = document.getElementById('form_area');
        let get_area = null;
        for (let i=0;i<get_cities.length;i++){
            if(get_cities[i]['cityCode']===city){
                get_area = get_cities[i]['counties']
            }
        }
        //console.log(get_area)
        form_area.options.add(new Option('区',''))
        for (let i=0;i<get_area.length;i++){

            let now_area = get_area[i]
            //console.log(now_area['cityName'])
            form_area.options.add(new Option(now_area['countyName'],now_area['countyCode']))

        }

    });

        let get_cities2 = null;
    $('#form_province2').change(function (){
        let province2 = $('#form_province2').val();
        $("#form_city2").empty();

        $("#form_area2").empty();
        get_cities2=null
        //console.log(province2)
        let form_city2 = document.getElementById('form_city2');

        for (let i=0;i<cities.length;i++){
            if(cities[i]['provinceCode']===province2){
                get_cities2 = cities[i]['cities']
            }
        }
        //console.log(get_cities2)
        form_city2.options.add(new Option('市',''))
        for (let i=0;i<get_cities2.length;i++){

            let now_city2 = get_cities2[i]
            //console.log(now_city2['cityName'])
            form_city2.options.add(new Option(now_city2['cityName'],now_city2['cityCode']))

        }

    });

        $('#form_city2').change(function (){
        let city2 = $('#form_city2').val();
        $("#form_area2").empty();

        let form_area2 = document.getElementById('form_area2');
        let get_area2 = null;
        for (let i=0;i<get_cities2.length;i++){
            if(get_cities2[i]['cityCode']===city2){
                get_area2 = get_cities2[i]['counties']
            }
        }

        form_area2.options.add(new Option('区',''))
        for (let i=0;i<get_area2.length;i++){

            let now_area2 = get_area2[i]
            //console.log(now_area2['cityName'])
            form_area2.options.add(new Option(now_area2['countyName'],now_area2['countyCode']))

        }

    });

    createProvince()




    function confirm_my_model(){
        $('#staticBackdrop').modal('hide')
        document.getElementById('audio_display').pause()
        let send_data = {
            "status":20100,
            "msg":"确认"
        }

        ws.send(JSON.stringify(send_data))
    }

        function cancel_my_model(){

        $('#staticBackdrop').modal('hide')
            document.getElementById('audio_display').pause()
        let send_data = {
            "status":20200,
            "msg":"取消"
        }
        ws.send(JSON.stringify(send_data))
    }

    function alert_notice_confirm(json_data){
        let new_json_data = {}
        let show_notice_div = $('#modal_body_id')
        show_notice_div.empty()
        document.getElementById('audio_display').play()
        if(json_data["mobile"]){
            new_json_data["手机号码"] = json_data["mobile"]
            $('#modal_footer_id').hidden
            document.title = "抢单成功"
            ws.close()
        }
        new_json_data["出发地"] = json_data["from_name"]
        new_json_data["到达地"] = json_data["to_name"]
        new_json_data["备注信息"] = json_data["description"]
        new_json_data["接货时间"] = json_data["goods_time"]
        new_json_data["价格"] = json_data["price"]
        console.log(json_data)


        $.each(
            new_json_data,function (k,v){
                show_notice_div.append("<p style='color: mediumpurple'>"+k+":"+v+"</p>")

            }
        )
        $('#staticBackdrop').modal('show')

    }

    // function alert_notice_result(json_data){
    //     let new_json_data = {}
    //     new_json_data["手机号码"] = json_data["mobile"]
    //     new_json_data["出发地"] = json_data["from_name"]
    //     new_json_data["到达地"] = json_data["to_name"]
    //     new_json_data["备注信息"] = json_data["description"]
    //     new_json_data["接货时间"] = json_data["goods_time"]
    //     new_json_data["价格"] = json_data["price"]
    //     console.log(json_data)
    //     let show_notice_div = $('#modal_body_id')
    //
    //     $.each(
    //         new_json_data,function (k,v){
    //             show_notice_div.append("<p style='color: mediumpurple'>"+k+":"+v+"</p>")
    //
    //         }
    //     )
    //     $('#staticBackdrop').modal('show')
    // }
