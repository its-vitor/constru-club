export default function getUserPoints() {
  const url = "http://127.0.0.1";
  const userPointsSpan = document.querySelector("#user-points");
  const userId = localStorage.key(0);

  async function userPoints() {
    const config = {
      method: "GET",
      headers: {
        Authorization: localStorage.getItem(userId),
      },
    };

    try {
      const req = await fetch(`${url}:80/user/points`, config);
      const res = await req.json();

      if (res.apiStatus === 200) {
        userPointsSpan.innerText = res.totalPoints;
      }
    } catch (error) {
      console.log(error);
    }
  }

  window.addEventListener("load", userPoints);
}
