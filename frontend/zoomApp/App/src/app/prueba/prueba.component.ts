import { Component, OnInit, ViewChild } from '@angular/core';
import { NgxCaptureService } from 'ngx-capture';
import { saveAs } from 'file-saver';
import { interval } from 'rxjs';
import { takeWhile } from 'rxjs/operators';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-prueba',
  templateUrl: './prueba.component.html',
  styleUrls: ['./prueba.component.css'],
})
export class PruebaComponent implements OnInit {
  @ViewChild('prueba', { static: true }) screen: any;
  imgBase64: any = '';
  recording = false;
  constructor(
    private captureService: NgxCaptureService,
    private api: ApiService
  ) {}

  ngOnInit(): void {}

  capture() {
    this.captureService
      .getImage(this.screen.nativeElement, true)
      .subscribe((img) => {
        this.imgBase64 = img;
        var imgB = img.split(',')[1];
        const formData = new FormData();
        formData.append('imageBase64', imgB);
        formData.append('meetingId', '12345678');
        console.log(formData);
        this.api.sortImageAttention(formData).subscribe((res: any) => {
          console.log(res);
        });
      });
  }

  startCapture(): void {
    if (this.recording == false) {
      this.recording = true;
      console.log('Inciando captura');
      interval(10000) // Ejecuta la función cada 30 segundos (30000 milisegundos)
        .pipe(takeWhile(() => this.captureEnabled)) // Continúa ejecutando mientras captureEnabled sea verdadero
        .subscribe(() => {
          this.capture();
        });
    } else {
      this.stopCapture();
    }
  }

  captureEnabled = true; // Variable para habilitar o deshabilitar la captura

  stopCapture(): void {
    this.captureEnabled = false; // Detiene la captura estableciendo captureEnabled a falso
  }
}
