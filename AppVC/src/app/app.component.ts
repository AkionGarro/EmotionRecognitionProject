import {
  Component,
  OnInit,
  Inject,
  ViewChild,
  ElementRef,
} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { DOCUMENT } from '@angular/common';
import { ZoomMtg } from '@zoomus/websdk';
import { NgxCaptureService } from 'ngx-capture';
import { saveAs } from 'file-saver';
import { interval } from 'rxjs';
import { takeWhile } from 'rxjs/operators';
import { ImageCapture } from 'image-capture';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
ZoomMtg.setZoomJSLib('https://source.zoom.us/2.13.0/lib', '/av');
ZoomMtg.preLoadWasm();
ZoomMtg.prepareWebSDK();
// loads language files, also passes any error messages to the ui
ZoomMtg.i18n.load('en-US');
ZoomMtg.i18n.reload('en-US');
import ZoomMtgEmbedded from '@zoomus/websdk/embedded';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {


  imgBase64: any = '';

  authEndpoint = '';
  sdkKey = 'UH3fpvIWRjeCFqEonE7xAQ';
  meetingNumber = '8089810074';
  passWord = '12345678';
  role = 0;
  userName = 'AkionGarro';
  userEmail = 'ikonikacc2908@gmail.com';
  registrantToken = '';
  zakToken = '';

  client = ZoomMtgEmbedded.createClient();

  constructor(
    public httpClient: HttpClient,
    @Inject(DOCUMENT) document,
    private captureService: NgxCaptureService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit() {
    let meetingSDKElement = document.getElementById('meetingSDKElement');

    this.client.init({
      debug: true,
      zoomAppRoot: meetingSDKElement,
      language: 'en-US',
      customize: {
        video: {
          isResizable: true,
          viewSizes: {
            default: {
              width: 1000,
              height: 600,
            },
            ribbon: {
              width: 300,
              height: 700,
            },
          },
        },
        meetingInfo: [
          'topic',
          'host',
          'mn',
          'pwd',
          'telPwd',
          'invite',
          'participant',
          'dc',
          'enctype',
        ],
        toolbar: {
          buttons: [
            {
              text: 'Custom Button',
              className: 'CustomButton',
              onClick: () => {
                console.log('custom button');
              },
            },
          ],
        },
      },
    });
  }

  getSignature() {
    const url = 'http://localhost:4000';
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    this.httpClient
      .post(
        url,
        {
          meetingNumber: this.meetingNumber,
          role: this.role,
        },
        { headers }
      )
      .toPromise()
      .then((data: any) => {
        if (data.signature) {
          console.log(data.signature);
          this.startMeeting(data.signature);
          this.startCapture();
        } else {
          console.log(data);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  startMeeting(signature) {
    this.client.join({
      signature: signature,
      sdkKey: this.sdkKey,
      meetingNumber: this.meetingNumber,
      password: this.passWord,
      userName: this.userName,
      userEmail: this.userEmail,
      tk: this.registrantToken,
      zak: this.zakToken,
    });
  }

  capture() {
    var screenS = document.getElementById('meetingSDKElement');
    this.captureService.getImage(screenS, true).subscribe((img) => {
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

  startCapture(): void {
    interval(30000) // Ejecuta la función cada 30 segundos (30000 milisegundos)
      .pipe(takeWhile(() => this.captureEnabled)) // Continúa ejecutando mientras captureEnabled sea verdadero
      .subscribe(() => {
        this.capture();
      });
  }

  captureEnabled = true; // Variable para habilitar o deshabilitar la captura

  stopCapture(): void {
    this.captureEnabled = false; // Detiene la captura estableciendo captureEnabled a falso
  }
}
