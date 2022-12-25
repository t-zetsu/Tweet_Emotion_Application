window.onload = function () {
    let context = document.querySelector("#emotion_circle").getContext('2d')
    new Chart(context, {
        type: 'pie',
        data: {
            labels: ["サーモン", "ハマチ", "マグロ", "サバ", "エンガワ"],
            datasets: [{
                backgroundColor: ["#fa8072", "#00ff7f", "#00bfff", "#a9a9a9", "#f5f5f5"],
                data: [60, 20, 15, 10, 5]
            }]
        },
        options: {
            responsive: false,
        }
    });
}

function()