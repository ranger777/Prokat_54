tool_info_block = document.getElementById("tool_info_block");
tool_info_yes = document.getElementById('tool_info_yes');
tool_info_no = document.getElementById('tool_info_no');
tool_info_edit = document.getElementById('tool_info_edit');

tool_local_block = document.getElementById("tool_local_block");
tool_local_yes = document.getElementById('tool_local_yes');
tool_local_no = document.getElementById('tool_local_no');
tool_local_edit = document.getElementById('tool_local_edit');


tool_info_edit.addEventListener("click", editToolInfo);
function editToolInfo(event){
    event.preventDefault()
    tool_info_block.readOnly = false;
    tool_info_block.style.border = '1px solid #000';
    tool_info_yes.style.display = 'block';
    tool_info_no.style.display = 'block';
    tool_info_edit.style.display = 'none';
}


tool_local_edit.addEventListener("click", editToolLocal);
function editToolLocal(event){
    event.preventDefault()
    tool_local_block.disabled = false;
    tool_local_block.style.border = '1px solid #000';
    tool_local_yes.style.display = 'block';
    tool_local_no.style.display = 'block';
    tool_local_edit.style.display = 'none';
}



//валидация текстареа
function validateTextarea(tool_info){
    re = /[*'"+?^${}()|\[\]\\]/;
    return re.test(String(tool_info));
}

tool_info_yes.addEventListener("click", yesToolLocal);
function yesToolLocal(event){
    tool_info = tool_info_block.value;
    console.log(tool_info);
    console.log(validateTextarea(tool_info));
    if (validateTextarea(tool_info)){
        event.preventDefault()
        alert( 'Введены недопустимые символы: *\'"+?^${}()|[]\\');
        return false;
    }
    console.log("валидно");
}
