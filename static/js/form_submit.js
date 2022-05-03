    function getFormData(eId) {
    let jq =  $("#" + eId)
    let inData = {};
    jq.find("input").each(function () {
        if ($(this).attr("name") != null) {
            //inData.push({"name": $(this).attr("name"), "value": $(this).val().trim()});
            inData[$(this).attr("name")] = $(this).val().trim()
        }
    });
    jq.find("select").each(function () {
        //inData.push({"name": $(this).attr("name"), "value": $(this).val().trim()});
        if($(this).val() != null){
            inData[$(this).attr("name")] = $(this).val().trim()
        }else {
            inData[$(this).attr("name")] = ''
        }
    });
    //inData.push({"name":'inputConfirm', "value":  $('#inputConfirm').bootstrapSwitch('state')});
    //inData.push({"name":'inputConfirm_mobile', "value":  $('#inputConfirm_mobile').bootstrapSwitch('state')});
    //inData.push({"name":'inputConfirmOpen', "value":  $('#inputConfirmOpen').bootstrapSwitch('state')});
    inData['inputConfirm'] = $('#inputConfirm').bootstrapSwitch('state');
    inData['inputConfirm_mobile'] = $('#inputConfirm_mobile').bootstrapSwitch('state');
    inData['inputConfirmOpen'] = $('#inputConfirmOpen').bootstrapSwitch('state');
    console.log(inData)
    return JSON.stringify(inData);
}