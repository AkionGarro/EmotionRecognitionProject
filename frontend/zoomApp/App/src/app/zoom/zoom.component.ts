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
  }

  startCapture(): void {
    interval(20000) // Ejecuta la función cada 30 segundos (30000 milisegundos)
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
  captureScreen() {
    const constraints = {
      video: true,
      preferCurrentTab: true,
      audio: false,
    };

    navigator.mediaDevices
      .getDisplayMedia(constraints)
      .then((stream) => {
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

            // Convertir el lienzo a formato PNG
            canvas.toBlob((blob: any) => {
              // Crear un enlace de descarga
              const link = document.createElement('a');
              link.href = URL.createObjectURL(blob);
              console.log(link.href);
              link.download = 'captura.png';

              // Simular clic en el enlace para iniciar la descarga
              link.click();

              // Limpiar el objeto URL creado
              URL.revokeObjectURL(link.href);
            }, 'image/png');
          })
          .catch((error: any) => {
            console.error('Error capturing screen:', error);
          })
          .finally(() => {
            stream.getVideoTracks()[0].stop();
          });
      })
      .catch((error) => {
        console.error('Error accessing screen:', error);
      });
  }

  sayHelloBackend() {
    this.api.getHelloFromBackend().subscribe((res) => {
      console.log(res);
    });
  }
  /*
  capture() {
    this.captureService
      .getImage(this.screen.nativeElement, true)
      .subscribe((img) => {
        console.log(img);
        this.imgBase64 = img;
        const blob = this.DataURIToBlob(this.imgBase64);
        this.downloadBlobAsPNG(blob, 'image.png');
      });
  }

  DataURIToBlob(dataURI: string) {
    const splitDataURI = dataURI.split(',');
    const byteString =
      splitDataURI[0].indexOf('base64') >= 0
        ? atob(splitDataURI[1])
        : decodeURI(splitDataURI[1]);
    const mimeString = splitDataURI[0].split(':')[1].split(';')[0];

    const ia = new Uint8Array(byteString.length);
    for (let i = 0; i < byteString.length; i++)
      ia[i] = byteString.charCodeAt(i);

    return new Blob([ia], { type: mimeString });
  }

  downloadBlobAsPNG(blob: Blob, filename: string) {
    saveAs(blob, filename);
  }

*/
}
