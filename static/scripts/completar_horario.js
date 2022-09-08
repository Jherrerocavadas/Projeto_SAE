
// Inserir ou alterar as aulas das boxes
function troca_aula(novo_valor, arquivo_json){
    const dia_aula = arquivo_json[0]; //ex: ["Segunda", "Segunda", "Terça", "Terça"]
    const horarios_materia = arquivo_json[1]; //ex: ["7h40 - 8h30", "8h30 - 9h20", "9h30 - 10h20", ...]
    const cor = arquivo_json[2]; // ex: "#ffffff"
    const abreviado = arquivo_json[3]; // ex: "Seg. no Des. de Aplic."

    for (let i in dia_aula){ // Array de dia e horário devem ter o mesmo tamanho(um horário para cada dia listado).
      console.log(`[id='${dia_aula[i]}'][name='${horarios_materia[i]}']`);
      box_aula = document.querySelector(`[id='${dia_aula[i]}'][name='${horarios_materia[i]}']`);
      console.log(box_aula);
      box_aula.parentNode.style.background = cor; //Alterar a cor de fundo da box
      box_aula.innerText = verifyAbreviado(novo_valor, abreviado);
    }
}

// Criar uma janela popup que vai exibir as matérias disponiveis

// Limpar o container de aulas possíveis
function Aulas_possiveis() {
    const is_container = document.getElementById("container_aulas_disponiveis");
    if (is_container) {
      is_container.style.background = 'green';
      is_container.innerText = ""

      var child = is_container.lastElementChild;
        while (child) {
            is_container.removeChild(child);
            child = is_container.lastElementChild;
        }
    }
}

// Adicionar as possibilidades de aulas no container de aulas possíveis
function add_aulas_possiveis(materia_valor, json_aulas){
  const container_aulas_disponiveis = document.getElementById("container_aulas_disponiveis");
  const aula_disponivel = document.createElement("div");
  aula_disponivel.setAttribute("id", "aula_disponivel");
  aula_disponivel.setAttribute("class", "aula_disponivel");
  aula_disponivel.innerText = verifyAbreviado(materia_valor, json_aulas[3]);
  aula_disponivel.addEventListener("click", function(){ troca_aula(materia_valor, json_aulas);} )
  container_aulas_disponiveis.appendChild(aula_disponivel)
}

// Gerar texto Abreviado
function verifyAbreviado(nome_completo, nome_abreviado) {
  //Altera o texto da box, inserindo o nome abreviado se o nome completo for maior que 30 caracteres
  if(nome_completo.length >= 22){
    return nome_abreviado
  }
  return nome_completo
}


function relacionar_aulas(materia_valor, json_aulas, dia_da_aula, horario_da_aula){
  const json_dia = json_aulas[0];
  const json_horario = json_aulas[1];
  for (var i in json_dia) {// Array de dia e horário devem ter o mesmo tamanho(um horário para cada dia listado).
    if(json_dia[i] == dia_da_aula){
      if(json_horario[i] == horario_da_aula){
        console.log("Aula: " + verifyAbreviado(materia_valor, json_aulas[3]))
        add_aulas_possiveis(materia_valor, json_aulas)
      }
    }
  }
}

// Ver de inserir a mensagem:
  // Não há matérias disponíveis para o dia selecionado!
// Caso não haja matérias disponíveis para o dia e horário



function irra(curso, id_caixa_aula){

  fetch('static/cursos_disciplinas.json')
    .then((response) => response.json())
    .then(function(json){
      const elementoPai = document.getElementById(id_caixa_aula);
      const dia_da_aula = elementoPai.firstElementChild.getAttribute("id"); // Será definido pela div
      const horario_da_aula = elementoPai.firstElementChild.getAttribute("name"); // Será definido pela div

      Aulas_possiveis(); // Resetar o container das aulas disponíveis
      // console.log(json); // Para verificar todo o arquivo JSON
      function gerar_json(json){
        for(const [key, value] of Object.entries(json[curso])) {
          if(key != "Sigla" && key != "Periodo"){
            for(const[materia_valor, horario_materia] of Object.entries(json[curso][key])){
              const arquivo_json = json[curso][key][materia_valor];
              relacionar_aulas(materia_valor, arquivo_json, dia_da_aula, horario_da_aula);
            }
          }
        }
      }
      gerar_json(json);
      }
    )
}
