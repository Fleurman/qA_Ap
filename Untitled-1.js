document.body.innerHTML = "";
fetch("http://localhost/api/query", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ prompt: "Quel outils utiliser pour développer un jeu ?", metadata:true })
}).then((response) => {
    const reader = response.body.getReader();
                
            reader.read().then(function pump({ done, value }) {
                
                if (done) {
						console.log("DONE");
                    return;
                }

                let raw = new TextDecoder().decode(value);

				console.log(raw);				

                if(typeof raw == "string"){
					if(raw.startsWith("#METADATA#")){
						console.log("METAS")
						metadatas = JSON.parse(raw.replace("#METADATA#",""));
						console.log(metadatas)
						return reader.read().then(pump);
					}else{
						document.body.innerHTML += raw;
						return reader.read().then(pump);
					}
                }else{
                    return;
                }
            });
  })