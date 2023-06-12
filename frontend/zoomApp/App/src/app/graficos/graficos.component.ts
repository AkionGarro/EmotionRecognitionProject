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
  constructor(private api: ApiService) {}

  chartData: any;
  engaged1: any[] = [];
  emotions: any[] = [];
  id1: any[] = [];

  async ngOnInit(): Promise<void> {
    let meetID: any;
    if (localStorage.getItem('meetingId') != null) {
      meetID = localStorage.getItem('meetingId');
    } else {
      meetID = '12345678';
    }
    const formData = new FormData();
    formData.append('meetingID', meetID);
    this.api.getChartsInfo(formData).subscribe((result: any) => {
      console.log(result);
      this.chartData = result;
      if (this.chartData != null) {
        this.engaged1.push(
          Object(this.chartData['EngagedInfo']['probability'])
        );
        this.emotions.push(Object.values(this.chartData['EmotionsInfo']));
        this.id1.push(Object(this.chartData['ID']));

        console.log(this.emotions);
        console.log(this.engaged1);
        this.RenderChart();
      }
    });
  }

  RenderChart() {
    const chart = new Chart('chartemotion', {
      type: 'bar',
      data: {
        labels: [
          'angry',
          'disgust',
          'fear',
          'happy',
          'neutral',
          'sad',
          'surprise',
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
