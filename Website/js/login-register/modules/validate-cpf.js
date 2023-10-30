export default class ValidarCpf {
  constructor(element) {
    this.element = element;
  }
  limpar(cpf) {
    return cpf.replace(/\D/g, '');
  }
  construir(cpf) {
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/g, '$1.$2.$3-$4');
  }
  formatar(cpf) {
    const cpfLimpo = this.limpar(cpf);
    return this.construir(cpfLimpo);
  }
  validar(cpf) {
    const matchCpf = cpf.match(/(?:\d{3}[-.\s]?){3}\d{2}/g);
    return (matchCpf && matchCpf[0] === cpf);
  }
  validarNaMudanca(cpfElement) {
    if(this.validar(cpfElement.value)) {
      cpfElement.value = this.formatar(cpfElement.value);
      cpfElement.nextElementSibling.classList = "d-none card-text font-weight-bold text-danger";
    } else {
      cpfElement.classList.add('erro');
      cpfElement.classList.remove('valido');
      cpfElement.nextElementSibling.classList = "d-block card-text font-weight-bold text-danger";
    }
  }
  adicionarEvento() {
    this.element.addEventListener('change', () => {
      this.validarNaMudanca(this.element);
    })
  }
  adicionarErroSpan() {
    const erroElement = document.createElement('span');
    erroElement.classList = "d-none card-text font-weight-bold text-danger";
    erroElement.innerText = 'CPF Inválido.';
    this.element.parentElement.insertBefore(erroElement, this.element.nextElementSibling);
  }
  iniciar() {
    this.adicionarEvento();
    this.adicionarErroSpan();
    return this;
  }
}