function chart_brand(brand, anger, disgust, fear, joy, sadness){
    var chart = new CanvasJS.Chart("chart-" + brand, {
        theme: "dark2",
        animationEnabled: true,
        title: {
            text: brand
        },
        data: [{
            type: "column",
            dataPoints: [
                { label: "Anger",  y: anger },
                { label: "Disgust", y: disgust },
                { label: "Fear", y: fear },
                { label: "Joy",  y: joy },
                { label: "Sadness",  y: sadness }
            ]
        }]
    });
    chart.render();
}