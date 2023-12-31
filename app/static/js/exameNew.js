function exameNew(questoes_json) {
	const addQuestaoElementToHTML = questao => {
		console.log(questoesSelecionadas)
		const novoElemeto = document.createElement("li")
		novoElemeto.innerHTML = `
            <div value="${questao.id}" class="mb-3 mt-3 card">
                <div class="card-header d-flex flex-row">
                    <div  class="nota-input-container input-group d-flex flex-row w-75">
                        <div class="input-group-text">Nota</div>
                        <input 
                            class="form-control w-sm-auto w-md-50" 
                            type="text" 
                            name="questao_nota_${questao.id}" 
                            pattern="[0-9]+([.][0-9]+)?"
                            onblur="this.value=validInputNumber(this.value)"
                            required
                            current-value="0"
                            value="0"
                        >
                    </div>
                    <div class="button-remover-container d-flex flex-row w-25 justify-content-end">
                        <div questao-id=${questao.id} class="button-remove btn btn-primary">Remover</div>
                    </div>
                </div>
                <div class="card-body">
                    <div>
                        <h6 class="card-title float-left">Enunciado</h6>
                        <p class="card-text ms-3 mb-1">${questao.enunciado}</p>
                    </div>
                    <div>
                        <h6 class="card-title float-left">Resposta</h6>
                        <p class="card-text ms-3 mb-1">${questao.resposta}</p>
                    </div>
                </div>  
            </div>
        `
		novoElemeto.classList.add("container")
		novoElemeto.setAttribute("li-questao-id", questao.id)
		questoesContainer.appendChild(novoElemeto)
	}

	const setNotaInput = questao => {
		// configura os inputs de notas
		const notaInput = document.querySelector(`input[name="questao_nota_${questao.id}"]`)
		const notaExame = document.getElementById("notaExame")

		notaInput.addEventListener("input", () => {
			const currentNota = parseFloat(notaInput.getAttribute("current-value"))
			let notaExameValor = parseFloat(notaExame.value)
			let novaNota = validInputNumber(notaInput.value)

			// subtrai o valor atual para atualizar o total
			notaExameValor -= currentNota
			// se a nova nota = 0, entao o nao existe valor para ser somado
			if (novaNota !== 0) {
				notaExameValor += novaNota
			}
			notaExame.value = notaExameValor.toFixed(2)
			notaInput.setAttribute("current-value", novaNota)
		})
	}

	const setRemoveButton = questao => {
		// handle remover questoes
		const questaoID = questao.id
		const button = document.querySelector(`.button-remove[questao-id="${questaoID}"]`)

		button.addEventListener("click", () => {
			questoesSelecionadas = questoesSelecionadas.filter(questao => questao.id != questaoID)

			// remove valor da nota total
			const notaExame = document.getElementById("notaExame")
			const notaInput = document.querySelector(`input[name="questao_nota_${questao.id}"]`)
			if (notaInput.value != "") {
				const notaTotal = parseFloat(notaExame.value) - parseFloat(notaInput.value)
				notaExame.value = notaTotal.toFixed(2)
			}

			// remove li element da lista ul
			ulElement = document.getElementById("questoesContainer")
			questaoLiElement = document.querySelector(`li[li-questao-id="${questaoID}"]`)
			ulElement.removeChild(questaoLiElement)
		})
	}

	const questoesContainer = document.getElementById("questoesContainer")
	const btnIncluir = document.getElementById("btnIncluir")
	let questoesSelecionadas = []

	btnIncluir.addEventListener("click", () => {
		const myModal = document.querySelector("#questoesModal")
		const bsModal = bootstrap.Modal.getInstance(myModal)
		bsModal.hide()

		const checkboxes = document.querySelectorAll("input[name=questoes]:checked")
		// const questoes_json = {{ questoes_json }}

		// adiciona questoes marcadas ao array questoesSelecionadas
		checkboxes.forEach(check => {
			const questaoID = check.value
			const questaoSelecionada = questoes_json.find(questao => questao.id == questaoID)
			// verifica se a questao ja esta no array
			const findQuestao = questoesSelecionadas.find(questao => questao.id == questaoID)
			console.log(findQuestao)

			// add questao se é valida e não existe no array
			if (questaoSelecionada && !findQuestao) {
				questoesSelecionadas.push(questaoSelecionada)
				addQuestaoElementToHTML(questaoSelecionada)
				setNotaInput(questaoSelecionada)
				setRemoveButton(questaoSelecionada)
			}
			// desmarca checkbox
			check.checked = false
		})
	})

	// handle form submition
	const form = document.querySelector("form")
	form.addEventListener("submit", e => {
		if (questoesSelecionadas.length === 0) {
			e.preventDefault()
			alert("O exame deve ter ao menos uma questao!")
			return
		}

		if (parseFloat(document.getElementById("notaExame").value) == 0) {
			e.preventDefault()
			alert("O exame não pode ter nota 0!")
			return
		}

		const questoesSelecionadasInput = document.getElementById("questoesSelecionadasInput")
		const questoesObject = []
		questoesSelecionadas.forEach(questao => {
			// pega o valor do input
			let notaQuestao = document.querySelector(`input[name="questao_nota_${questao.id}"]`).value
			notaQuestao === "" ? (notaQuestao = 0) : (notaQuestao = parseFloat(notaQuestao))
			const obj = {
				questao_id: questao.id,
				nota_questao: notaQuestao,
			}

			questoesObject.push(obj)
		})
		questoesSelecionadasInput.value = JSON.stringify(questoesObject)
	})
}
