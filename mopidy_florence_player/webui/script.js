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
                            document.querySelector("#station_1_tracklist_placeholder").innerHTML = tag["parameter"];
                            document.querySelector("#station_1_alias_placeholder").innerHTML = tag["alias"];
                            break;
                        case 'station_2':
                            document.querySelector("#station_2_tracklist_placeholder").innerHTML = tag["parameter"];
                            document.querySelector("#station_2_alias_placeholder").innerHTML = tag["alias"];
                            break;
                        case 'station_3':
                            document.querySelector("#station_3_tracklist_placeholder").innerHTML = tag["parameter"];
                            document.querySelector("#station_3_alias_placeholder").innerHTML = tag["alias"];
                            break;
                        case 'station_4':
                            document.querySelector("#station_4_tracklist_placeholder").innerHTML = tag["parameter"];
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

    switch (s1) {
        case true: {
            station_1_class = "success"
            break
        }
        case "error": {
            station_1_class = "error"
            break
        }
    }
    switch (s2) {
        case true: {
            station_2_class = "success"
            break
        }
        case "error": {
            station_2_class = "error"
            break
        }
    }
    switch (s3) {
        case true: {
            station_3_class = "success"
            break
        }
        case "error": {
            station_3_class = "error"
            break
        }
    }
    switch (s4) {
        case true: {
            station_4_class = "success"
            break
        }
        case "error": {
            station_4_class = "error"
            break
        }
    }
    document.querySelector("#station_1").className = station_1_class
    document.querySelector("#station_2").className = station_2_class
    document.querySelector("#station_3").className = station_3_class
    document.querySelector("#station_4").className = station_4_class
}

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
