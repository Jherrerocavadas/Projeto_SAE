verificar_horario();

function troca_aula(id_caixa_aula, novo_valor){
    document.getElementById(id_caixa_aula).innerText = novo_valor;
    verificar_horario();
}

function verificar_horario(){


  fetch('static/cursos_disciplinas.json')
  //((arg)=> command) equivalente a:
  // (function(arg){command})
    // var arquivo_json;

    .then((response) => response.json())

    .then(function(json){
      var curso = "Design de Mídias Digitais" //Para testes
      // talvez inserir a lógica aqui
      function get_day(json){

        for (const [key, value] of Object.entries(json[curso])) {

            // console.log(Object.entries(json[curso]));
            // console.log("key: " + key);
            // console.log("value: " + value);
            if(key != "Sigla"){

              for(const[materia_valor, horario_materia] of Object.entries(json[curso][key])){
                console.log("materia_valor: " + materia_valor); //ex: Matemática discreta
                console.log("horario_materia: " + horario_materia); //ex: Segunda, Segunda...,7h40-8h30,...
                var json_gigante = json[curso][key][materia_valor];
                var json_dia = json_gigante[0]
                var json_horario = json_gigante[1]
                var dia_da_aula = "Segunda";
                var horario_da_aula = "7h40 - 8h30";
                console.log(json_gigante)

                function relacionar_day(dia_da_aula, horario_da_aula){

                    for (var i in json_dia) {//Dia
                        console.log("i é:" + i);
                        console.log("json_gigamesco é:" + json_dia[i]);
                        if(json_dia[i] == dia_da_aula){
                            console.log("Tem "+ materia_valor + " na "+ dia_da_aula);
                            for (var j in json_horario) {//Horário
                                console.log("j é:" + j);
                                console.log("json_do_horario é:" + json_horario[j]);
                              if(json_horario[j] == horario_da_aula){
                                console.log("Tem "+ materia_valor + " às "+ horario_da_aula);
                              }
                            };
                        }
                    };
                  };
                  relacionar_day(dia_da_aula, horario_da_aula);
              }

            } else {
              console.log("IRRA")
            }

        }
        // return json[curso]
      }







      get_day(json);
      }
    )

    // .then(function(json) {
    //    arquivo_json = json;
    //   return json;
    // })


}
