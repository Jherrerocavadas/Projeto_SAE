

function troca_aula(novo_valor, arquivo_json){
    dia_aula = arquivo_json[0]; //ex: ["Segunda", "Segunda", "Terça", "Terça"]
    horarios_materia = arquivo_json[1]; //ex: ["7h40 - 8h30", "8h30 - 9h20", "9h30 - 10h20", ...]
    cor = arquivo_json[2]; // ex: "#ffffff"
    abreviado = arquivo_json[3]; // ex: "Seg. no Des. de Aplic."

    // Ver de chamar o relacionar_day aqui
      for (var i in dia_aula){
          console.log(`Id: ${dia_aula[i]}]`);
          console.log(`[Name: ${horarios_materia[i]}]`);
          box_aula = document.querySelector(`[id='${dia_aula[i]}'][name='${horarios_materia[i]}']`);
          console.log("Horário é: " + box_aula.getAttribute("name"));
          console.log("Dia é: " + box_aula.getAttribute("id"));
          box_aula.parentNode.style.background = cor;
          box_aula.innerText = novo_valor;
          if(novo_valor.length > 30){
            box_aula.innerText = abreviado;
          }

          // }

      }

}

// Criar uma janela popup que vai exibir as matérias disponiveis
function Aulas_possiveis() {
    is_container = document.getElementById("container_aulas_disponiveis");
    if (is_container) {
      is_container.style.background = 'green';

      var child = is_container.lastElementChild;
        while (child) {
            is_container.removeChild(child);
            child = is_container.lastElementChild;
        }
    }

}

function add_aulas_possiveis(elementoPai, materia_valor, json_aulas, id_caixa_aula){

  container_aulas_disponiveis = document.getElementById("container_aulas_disponiveis");
  aula_disponivel = document.createElement("div");
  aula_disponivel.setAttribute("id", "aula_disponivel");
  aula_disponivel.setAttribute("class", "aula_disponivel");
  aula_disponivel.innerText = materia_valor
  // console.log(aula_disponivel.textContent)
  aula_disponivel.addEventListener("click", function(){ troca_aula(materia_valor, json_aulas);} )
  // aula_disponivel.onclick = function(){ troca_aula(elementoPai, aula_disponivel.textContent, json_aulas[3], json_aulas[2]);}
  container_aulas_disponiveis.appendChild(aula_disponivel)
}

function irra(curso, id_caixa_aula){


  fetch('static/cursos_disciplinas.json')
    .then((response) => response.json())
    .then(function(json){
      var elementoPai = document.getElementById(id_caixa_aula);
      Aulas_possiveis();

      function gerar_json(json){
        for (const [key, value] of Object.entries(json[curso])) {
            if(key != "Sigla" && key != "Periodo"){

              for(const[materia_valor, horario_materia] of Object.entries(json[curso][key])){
                // console.log("materia_valor: " + materia_valor); //ex: Matemática discreta
                // console.log("horario_materia: " + horario_materia); //ex: Segunda, Segunda...,7h40-8h30,...
                var arquivo_json = json[curso][key][materia_valor];
                var json_dia = arquivo_json[0];
                var json_horario = arquivo_json[1];
                var json_cor = arquivo_json[2];
                var dia_da_aula = elementoPai.firstElementChild.getAttribute("id"); // Será definido pela div
                var horario_da_aula = elementoPai.firstElementChild.getAttribute("name"); // Será definido pela div

                // talvez dar um return aqui e colocar a outra função em outra parte

                function relacionar_day(dia_da_aula, horario_da_aula){

                    for (var i in json_dia) {//Dia
                        // console.log("i é:" + i);
                        // console.log("json_gigamesco é:" + json_dia[i]);
                        if(json_dia[i] == dia_da_aula){
                            // console.log("Tem "+ materia_valor + " na "+ dia_da_aula);
                            if(json_horario[i] == horario_da_aula){
                                // console.log("Tem "+ materia_valor + " às "+ horario_da_aula);

                                // Mostra as aulas disponíveis
                                console.log("Aula: " + materia_valor)
                                add_aulas_possiveis(elementoPai, materia_valor, arquivo_json, id_caixa_aula)
                                // return troca_aula(elementoPai, materia_valor,arquivo_json[3], json_cor);
                                // break;
                              }
                        }
                        // console.log("saiu do if")
                    };
                  };
                  relacionar_day(dia_da_aula, horario_da_aula);
                  // break;
              }

            }

        }
      }
      gerar_json(json);
      }
    )
}
