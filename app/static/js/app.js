document.getElementById("select").onclick = function () {      
    var value = document.getElementById("select").innerHTML
    if (value == "Select all albums") {
        document.getElementById("select").innerHTML = "Deselect all albums";
        checks = true;
    } else {
        document.getElementById("select").innerHTML = "Select all albums";
        checks = false;
    }

    
    allboxes = document.getElementsByName("album");
    for (var i = 0; i < allboxes.length; i++) {               
        allboxes[i].checked = checks;
    }  
};

document.getElementById("send").onclick = function () {
    if (GetCheckedCount() > 0) {
        document.forms[0].submit();
    } else {
        document.getElementById("thesong").innerHTML = "<p>** Please, select one or more albums **</p>";
    }
};

function GetCheckedCount() {
    var inputList = document.getElementsByTagName("input");
    var checkedCount = 0;
    for (var i = 0; i < inputList.length; i++) {
        if (inputList[i].type == "checkbox" && inputList[i].checked) {
            checkedCount += 1;
        }
    }
    return checkedCount;   
};
