import { Component, OnInit } from '@angular/core';
import Swal from 'sweetalert2';
import { interval } from 'rxjs';
import { takeWhile } from 'rxjs/operators';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { ImageCapture } from 'image-capture';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-zoom',
  templateUrl: './zoom.component.html',
  styleUrls: ['./zoom.component.css'],
})
export class ZoomComponent implements OnInit {
  meetingId: string = '';
  password: string = '';

  ngOnInit(): void {}
  constructor(private sanitizer: DomSanitizer, private api: ApiService) {}
  async onJoinClick() {
    if (this.meetingId === '' || this.password === '') {
      Swal.fire({
        icon: 'error',
        title: 'Ha ocurrido un error',
        text: 'Complete los campos para continuar',
      });
      return;
    } else {
      this.joinMeeting(this.meetingId, this.password);
    }
  }

  async joinMeeting(meeting: string, passWordI: string): Promise<any> {
    const { ZoomMtg } = await import('@zoomus/websdk');
    ZoomMtg.setZoomJSLib('https://source.zoom.us/lib', '/av');
    ZoomMtg.preLoadWasm();
    ZoomMtg.prepareWebSDK();

    let payload = {
      meetingNumber: meeting,
      passWord: passWordI,
      sdkKey: 'UH3fpvIWRjeCFqEonE7xAQ',
      sdkSecret: 'b28jDoAI6BfR96tcGf7p1BWLYmbJFdG4',
      userName: 'Akion',
      userEmail: '',
      leaveUrl: 'http://localhost:4200',
      role: '0',
    };

    ZoomMtg.generateSDKSignature({
      meetingNumber: payload.meetingNumber,
      role: payload.role,
      sdkKey: payload.sdkKey,
      sdkSecret: payload.sdkSecret,
      success: function (signature: any) {
        ZoomMtg.init({
          leaveUrl: payload.leaveUrl,
          success: function (data: any) {
            ZoomMtg.join({
              meetingNumber: payload.meetingNumber,
              passWord: payload.passWord,
              userName: payload.userName,
              userEmail: payload.userEmail,
              sdkKey: payload.sdkKey,
              signature: signature.result,
              tk: '',
              success: function (res: any) {
                console.log(res);
              },
              error: function (error: any) {
                console.log('Error Join --->', error);
              },
            });
          },
          error: function (error: any) {
            console.log('Error init --->', error);
          },
        });
      },
      error: function (error: any) {
        console.log('Error --->', error);
      },
    });
    localStorage.setItem('meetingId', meeting);
    this.startCapture();
  }

  startCapture(): void {
    interval(60000) // Ejecuta la función cada 60 segundos (30000 milisegundos)
      .pipe(takeWhile(() => this.captureEnabled)) // Continúa ejecutando mientras captureEnabled sea verdadero
      .subscribe(() => {
        this.captureScreen();
      });
  }

  captureEnabled = true; // Variable para habilitar o deshabilitar la captura

  stopCapture(): void {
    this.captureEnabled = false; // Detiene la captura estableciendo captureEnabled a falso
  }

  //Segunda funcion para capturar pantalla
  async captureScreen() {
    const constraints = {
      video: true,
      preferCurrentTab: true,
      audio: false,
    };

    navigator.mediaDevices.getDisplayMedia(constraints).then((stream) => {
      const videoTrack = stream.getVideoTracks()[0];
      const imageCapture = new ImageCapture(videoTrack);

      imageCapture
        .grabFrame()
        .then((imageBitmap: any) => {
          const canvas = document.createElement('canvas');
          canvas.width = imageBitmap.width;
          canvas.height = imageBitmap.height;
          const ctx = canvas.getContext('2d');
          ctx?.drawImage(imageBitmap, 0, 0);

          // Convert the canvas to a Base64-encoded string
          const dataUrl = canvas.toDataURL();

          // Extract the Base64-encoded image data from the data URL
          const base64Image = dataUrl.split(',')[1];

          console.log(base64Image);
          const formData = new FormData();
          formData.append('imageBase64', base64Image);
          formData.append('meetingId', this.meetingId);
          console.log(formData);
          this.api.sortImageAttention(formData).subscribe((res) => {
            console.log(res);
          });
        })
        .catch((error: any) => {
          console.error('Error capturing screen:', error);
        })
        .finally(() => {
          stream.getVideoTracks()[0].stop();
        });
    });
  }

  sayHelloBackend() {
    this.api.getHelloFromBackend().subscribe((res) => {
      console.log(res);
    });
  }
}
