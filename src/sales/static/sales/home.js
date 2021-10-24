console.log("hello word")
const reportBtn = document.getElementById("report-btn")
const img = document.getElementById("img")
const modalBody = document.getElementById('modal-body')
const id_name = document.getElementById('id_name')
const id_remarks = document.getElementById('id_remarks')
const csrf= document.getElementsByName('csrfmiddlewaretoken')[0].value
const reportForm = document.getElementById('report-form')

console.log(reportBtn)
console.log(img)

if(img){
    reportBtn.classList.remove("not-visible")
}

reportBtn.addEventListener('click',()=>{
    console.log('clicked')
    img.setAttribute('class','w-100')
    modalBody.prepend(img) 

    reportForm.addEventListener('submit',e=>{
        e.preventDefault()
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken',csrf)
        formData.append('name',id_name.value)
        formData.append('remarks',id_remarks.value)
        formData.append('image',img.src)

        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data:formData,
            success:function(response){
                console.log(response)
            },
            error:function(error){
                console.log(error)
            },
            processData:false,
            contentType:false,
        })
    })
})