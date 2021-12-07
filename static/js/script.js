// 画像のプレビュー表示
function previewImage(obj)
{
    var fileReader = new FileReader();
    fileReader.onload = (function() {
        document.getElementById('preview').src = fileReader.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}

// ボタンで表示変更
function changeDisplay() {
    var obj = document.getElementById('history');
    state = obj.style.display;
    console.log(state);
    if( state=="none" ){
        obj.setAttribute("style","display:inline");
        console.log("inline");
    }
    else {
        obj.setAttribute("style","display:none");
        console.log("none");
     }
 }