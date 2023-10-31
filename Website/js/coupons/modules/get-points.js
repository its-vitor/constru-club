export default function getPoints() {
  const url = "https://construclub.squareweb.app";
  const pointsSpan = document.querySelector("#points");
  const userId = localStorage.key(0);
  const logout = document.querySelector("#logoutBtn");

  function handleClick() {
    localStorage.removeItem(userId);
    location = `${url}:5500`;
  }

  async function points() {
    const config = {
      method: "GET",
      headers: {
        Authorization: localStorage.getItem(userId),
      },
    };

    try {
      const req = await fetch(`${url}/total/points`, config);
      const res = await req.json();
      pointsSpan.innerText = res.totalPoints;
    } catch (error) {
      console.log(error);
      const tryAgain = confirm(
        "Você não está logado. Deseja voltar para a tela de login e tentar novamente?"
      );

      tryAgain ? (location.href = `${url}:5500`) : null;
    }
  }

  window.addEventListener("load", points);
  logout.addEventListener("click", handleClick);
}
