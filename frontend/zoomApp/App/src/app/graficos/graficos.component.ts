import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { ApiService } from '../services/api.service';
@Component({
  selector: 'app-graficos',
  templateUrl: './graficos.component.html',
  styleUrls: ['./graficos.component.css'],
})
export class GraficosComponent implements OnInit {
  constructor(private http: HttpClient, private api :ApiService) {}

  chartData: any;
  engaged1: any[] = [];
  emotions: any[] = [];
  id1: any[] = [];

  ngOnInit(): void {
    this.getChartInfo().subscribe((result) => {
      this.chartData = result;

      if (this.chartData != null) {
        /* for(let i=0; i<this.chartData.length; i++){
          //console.log(this.chartData[i]);
          //this.engaged1.push(this.chartData[i].engaged)
          this.engaged1.push(Object.values(this.chartData[i].Emotion))
          
        } */
        this.engaged1.push(
          Object(this.chartData[this.chartData.length - 1].Engaged)
        );
        this.emotions.push(
          Object.values(this.chartData[this.chartData.length - 1].Emotion)
        );
        this.id1.push(
          Object.values(this.chartData[this.chartData.length - 1].id)
        );

        console.log(this.emotions);
        console.log(this.engaged1);
        this.RenderChart();
      }
    });
  }
  getChartInfo() {
    return this.http.get('http://localhost:3000/charts');
  }
  RenderChart() {
    const chart = new Chart('chartemotion', {
      type: 'bar',
      data: {
        labels: [
          'Angry',
          ' Disgust',
          'Fear',
          'Happy',
          'Sad',
          'Surprise',
          'Neutral',
        ],
        datasets: [
          {
            label: 'Emociones',
            data: [
              this.emotions[0][0],
              this.emotions[0][1],
              this.emotions[0][2],
              this.emotions[0][3],
              this.emotions[0][4],
              this.emotions[0][5],
              this.emotions[0][6],
            ],
            backgroundColor: ['#00B4FF'],
            borderColor: ['#00B4FF'],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
    const chart1 = new Chart('chartengaged', {
      type: 'pie',
      data: {
        labels: ['Engaged', 'NotEngaged'],
        datasets: [
          {
            label: 'Engaged',
            data: [this.engaged1, 1 - Number(this.engaged1)],
            backgroundColor: ['#4CFF00', '#FF4100'],
            borderColor: ['#4CFF00', '#FF4100'],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
}
