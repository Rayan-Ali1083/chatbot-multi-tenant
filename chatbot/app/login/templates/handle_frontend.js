    
    function open_modal(id, context) {
        document.getElementById('edit-text-value').value = context;
        document.getElementById('edit-area').classList.remove('hidden');
    }
    
    
    
        function close_modal() {
          document.getElementById('edit-text-value').value = '';
    
          document.getElementById('edit-area').classList.add('hidden');
        }
    
        function handle_select(option) {
          console.log(option);
          if (option == 'toggle_upload') {
            document.getElementById("uploadarea").classList.toggle("hidden");
            document.getElementById("textupload").classList.add("hidden");
          } else if (option == 'edit') {
            document.getElementById("textupload").classList.toggle("hidden");
            document.getElementById("uploadarea").classList.add("hidden");
          } else {
            console.log("Invalid option");
          }
          document.getElementById('select').selectedIndex = 0;
    
        };
    
    
        function textsubmit() {
          var text = document.getElementById("textupload_value");
          console.log(text.value);
    
          if (text.value === "") {
            alert("Please enter some text to upload.");
            return;
          } else {
            collection_name = "{{ collection_name }}";
            document.getElementById("textupload_value").value = "";
            document.getElementById("textupload").classList.toggle("hidden");
            text = document.getElementById("textupload_value");
    
            const response = fetch('http://52.21.238.142:1024/add_doc', {
              method: 'POST',
              body: JSON.stringify({
                text: text,
                collection_name: collection_name
              }),
              mode: 'no-cors',
              headers: {
                'Content-Type': 'application/json'
              }
            });
          }
    
        }
    
        const fileTempl = document.getElementById("file-template"),
          imageTempl = document.getElementById("image-template"),
          empty = document.getElementById("empty");
    
        let FILES = {};
    
        function addFile(target, file) {
          const objectURL = URL.createObjectURL(file);
    
          const clone = fileTempl.content.cloneNode(true);
    
          clone.querySelector("h1").textContent = file.name;
    
          clone.querySelector("li").id = objectURL;
    
          clone.querySelector(".delete").dataset.target = objectURL;
    
          clone.querySelector(".size").textContent =
            file.size > 1024 ?
            file.size > 1048576 ?
            Math.round(file.size / 1048576) + "mb" :
            Math.round(file.size / 1024) + "kb" :
            file.size + "b";
    
          empty.classList.add("hidden");
    
          target.prepend(clone);
    
          FILES[objectURL] = file;
    
        }
    
    
        // document.getElementById("form").onsubmit = (e) => {
        // e.preventDefault();
    
        const formData = new FormData();
        for (const key in FILES) {
          formData.append('files', FILES[key]);
          console.log(FILES[key]);
        }
    
    
        const gallery = document.getElementById("gallery"),
          overlay = document.getElementById("overlay");
    
        const hidden = document.getElementById("hidden-input");
        document.getElementById("button").onclick = () => hidden.click();
        hidden.onchange = (e) => {
          for (const file of e.target.files) {
            addFile(gallery, file);
          }
        };
    
        const hasFiles = ({
            dataTransfer: {
              types = ['']
            }
          }) =>
          types.indexOf("Files") > -1;
    
        let counter = 0;
    
        function dropHandler(ev) {
          ev.preventDefault();
          for (const file of ev.dataTransfer.files) {
            addFile(gallery, file);
            overlay.classList.remove("draggedover");
            counter = 0;
          }
        }
    
        // only react to actual files being dragged
        function dragEnterHandler(e) {
          e.preventDefault();
          if (!hasFiles(e)) {
            return;
          }
          ++counter && overlay.classList.add("draggedover");
        }
    
        function dragLeaveHandler(e) {
          1 > --counter && overlay.classList.remove("draggedover");
        }
    
        function dragOverHandler(e) {
          if (hasFiles(e)) {
            e.preventDefault();
          }
        }
    
        // event delegation to caputre delete events
        // fron the waste buckets in the file preview cards
        gallery.onclick = ({
          target
        }) => {
          if (target.classList.contains("delete")) {
            const ou = target.dataset.target;
            document.getElementById(ou).remove(ou);
            gallery.children.length === 1 && empty.classList.remove("hidden");
            delete FILES[ou];
          }
        };
    
    
    
        // clear entire selection
        document.getElementById("cancel").onclick = () => {
          while (gallery.children.length > 0) {
            gallery.lastChild.remove();
          }
          FILES = {};
          empty.classList.remove("hidden");
          gallery.append(empty);
    
          document.getElementById("uploadarea").classList.toggle("hidden");
        };