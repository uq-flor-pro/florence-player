/*
 * API class which communicates with the Florence Player REST API.
 */

class API {

    /*
     * Send AJAX request to REST API endpoint.
     */

    request = (endpoint, data, callback) => {
        let init = {}
        if(data)
            init = { method: 'POST', body: data }

        fetch(endpoint, init)
        .then((response) => {
            return response.json()
        })
        .then(callback)

    }

    /*
     * Refresh the registry.
     */

    refreshRegistry = () => {
        let callback = (response) => {
            let tagsContainer = document.getElementById('tags')
            while(tagsContainer.firstChild) {
                tagsContainer.removeChild(tagsContainer.firstChild)
            }

            for(let tag of response.tags) {
                let tagElement
                // tag is a either an RFID tag or a station. both are stored in the registry the only
                // difference is the format of the identifier. stations are of the form "station_x"
                // where x \in {1,2,3,4}
                if (!tag["uid"].startsWith("station_")) {
                    // tag is an rfid tag
                    tagElement = document.createElement('div')
                    tagElement.setAttribute('class', 'tag')
                }
                let args = new Array('alias', 'uid', 'action_class', 'parameter')
                for(let arg of args) {
                    let spanElement = document.createElement('span')
                    let value       = tag[arg] ? tag[arg] : '-'
                    spanElement.setAttribute('class', arg.replace('_', '-'))
                    spanElement.innerHTML = value
                    switch (tag['uid']) {
                        case 'station_1':
                            document.querySelector("#station_1_tracklist_placeholder").innerHTML = "<a href='" +
                                tag["parameter"] + "'>" + tag["parameter"] + "</a>"
                            document.querySelector("#station_1_alias_placeholder").innerHTML = tag["alias"];
                            break;
                        case 'station_2':
                            document.querySelector("#station_2_tracklist_placeholder").innerHTML = "<a href='" +
                                tag["parameter"] + "'>" + tag["parameter"] + "</a>"
                            document.querySelector("#station_2_alias_placeholder").innerHTML = tag["alias"];
                            break;
                        case 'station_3':
                            document.querySelector("#station_3_tracklist_placeholder").innerHTML = "<a href='" +
                                tag["parameter"] + "'>" + tag["parameter"] + "</a>"
                            document.querySelector("#station_3_alias_placeholder").innerHTML = tag["alias"];
                            break;
                        case 'station_4':
                            document.querySelector("#station_4_tracklist_placeholder").innerHTML = "<a href='" +
                                tag["parameter"] + "'>" + tag["parameter"] + "</a>"
                            document.querySelector("#station_4_alias_placeholder").innerHTML = tag["alias"];
                            break;
                        default:
                            tagElement.appendChild(spanElement)
                    }

                }
                if (!tag["uid"].startsWith("station_")) {
                    // it is a RFID tag not a station so display it
                    tagsContainer.appendChild(tagElement)
                }
            }
        }

        this.request('/florence/registry/', false, callback)
    }

    /*
     * Refresh the tags.
     */

    refreshActionClasses = () => {
        let callback = (response) => {
            let select = document.getElementById('action-class');
            while(select.firstChild)
                select.removeChild(select.firstChild)

            for(let action_class in response.action_classes) {
                let option = document.createElement('option')
                option.setAttribute('value', action_class)
                option.innerHTML = action_class + ' (' + response.action_classes[action_class] + ')'
                select.appendChild(option)
            }
        }

        this.request('/florence/action-classes/', false, callback)
    }

    /*
     * Reset the form.
     */

    formCallback = (response) => {
        if(response.success) {
            this.refreshRegistry()
            document.getElementById('uid').value                = ''
            document.getElementById('alias').value              = ''
            document.getElementById('parameter').value          = ''
            document.getElementById('action-class').selectIndex = 0
	    handle_station_response(response.station_1, response.station_2, response.station_3, response.station_4)
        } else {
            window.alert(response.message)
        }
    }

    /*
     * Register a new tag.
     */

    register = () => {
        let form = document.getElementById('register-form')
        let data = new FormData(form)
        this.request('/florence/register/', data, this.formCallback)
    }
    
    register_stations = () => {
        let form = document.getElementById('register-stations-form')
        let data = new FormData(form)
        this.request('/florence/registerstations/', data, this.formCallback)
    }

    /*
     * Unregister an existing tag.
     */

    unregister = () => {
        let form = document.getElementById('register-form')
        let data = new FormData(form)
        this.request('/florence/unregister/', data, this.formCallback)
    }

    /*
     * Get latest scanned tag.
     */

    getLatestTag = () => {
        let latest_tag = undefined

        let uid_field           = document.getElementById('uid')
        let alias_field         = document.getElementById('alias')
        let parameter_field     = document.getElementById('parameter')
        let action_class_select = document.getElementById('action-class')

        uid_field.value              = ''
        alias_field.value            = ''
        parameter_field.value        = ''
        action_class_select.selectIndex = 0

        let link = document.getElementById('read-rfid-tag')
        link.classList.add('reading')

        let do_request = () => {
            let callback = (response) => {
                if(latest_tag && response.success && JSON.stringify(response) != JSON.stringify(latest_tag)) {
                    uid_field.value = response.uid

                    if(response.alias)
                        alias_field.value = response.alias

                    if(response.parameter)
                        parameter_field.value = response.parameter

                    if(response.action_class)
                        action_class_select.value = response.action_class

                    link.classList.remove('reading')
                } else {
                    setTimeout(() => do_request(), 1000)
                }

                latest_tag = response
            }

            api.request('/florence/latest/', false, callback)
        }

        do_request()
    }

}

function handle_station_response(s1, s2, s3, s4) {
    var station_1_class, station_2_class, station_3_class, station_4_class

    s1 === true ? station_1_class = "card success" : station_1_class = "card " + s1
    s2 === true ? station_2_class = "card success" : station_2_class = "card " + s2
    s3 === true ? station_3_class = "card success" : station_3_class = "card " + s3
    s4 === true ? station_4_class = "card success" : station_4_class = "card " + s4

    document.querySelector("#station_1").className = station_1_class
    document.querySelector("#station_2").className = station_2_class
    document.querySelector("#station_3").className = station_3_class
    document.querySelector("#station_4").className = station_4_class

    document.getElementById('register-stations-form').reset();
}

// https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop
function dragOverHandler(ev) {
    console.log('File(s) in drop zone');
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
}

function dropHandler(ev) {
    console.log('File(s) dropped');

    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
    if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (let i = 0; i < ev.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if (ev.dataTransfer.items[i].kind === 'file') {
                const file = ev.dataTransfer.items[i].getAsFile();
                filelist.push(file);
            }
        }
    } else {
        // Use DataTransfer interface to access the file(s)
            for (let i = 0; i < ev.dataTransfer.files.length; i++) {
                filelist.push(ev.dataTransfer.files[i]);
            }
    }
  document.querySelector("#filelist").innerHTML = ""

  for (var f of filelist) {
      var li = document.createElement("li");
      li.innerHTML = f.name
      document.querySelector("#filelist").appendChild(li)
  }
}

async function sendFiles() {
    document.querySelector("#draganddropsend").innerHTML = "Sending... please wait."
    for (var f of filelist) {
        try {
            let result = await uploadFile(f);
        } catch {
            alert("One or more files failed to upload. Valid filetypes are mp3, wav, flac and zip, and maximum size is 100Mb.")
            break
        }
    }
    // reset interface
    filelist = []
    document.querySelector("#filelist").innerHTML = "Nothing yet."
    document.querySelector("#draganddropsend").innerHTML = "✓ Send Files"
    alert('File(s) successfully uploaded')
}

// https://stackoverflow.com/questions/48969495/in-javascript-how-do-i-should-i-use-async-await-with-xmlhttprequest
function uploadFile(file) {
    return new Promise(function (resolve, reject) {
        var url = '/florence/upload/file'
        var xhr = new XMLHttpRequest()
        var formData = new FormData()
        xhr.open('POST', url, true)
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject("Error");
            }
        }
        formData.append('file1', file)
        xhr.send(formData)
    });
}

async function sendFromInput() {
    document.querySelector("#inputsend").innerHTML = "Sending... please wait."
    for (var file of document.querySelector("#filesInput").files) {
        try {
            let result = await uploadFile(file);
        } catch {
            alert("One or more files failed to upload. Valid filetypes are mp3, wav, flac and zip, and maximum size is 100Mb.")
            break
        }
    }
    // reset interface
    document.querySelector("#filesInput").value = null
    document.querySelector("#inputsend").innerHTML = "✓ Send Files"
    alert('File(s) successfully uploaded')
}

/* start */

var filelist = []

api = new API()

api.refreshRegistry()
api.refreshActionClasses()

document.addEventListener('click', (event) => {
    let target = event.target
    let div    = target.closest('div')

    if(div && div.classList.contains('tag')) {
        for(let child of div.children) {
            document.getElementById(child.className).value = child.innerHTML.replace(/^-$/, '')
        }
    }
})

document.getElementById('register-form').onsubmit = () => {
    api.register()
    return false;
}

document.getElementById('unregister-button').onclick = () => {
    api.unregister()
    return false
}

document.getElementById('read-rfid-tag').onclick = () => api.getLatestTag()

document.getElementById('register-stations-form').onsubmit = () => {
    api.register_stations()
    return false;
}
