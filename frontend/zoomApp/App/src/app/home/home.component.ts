import { Component, OnInit, ViewChild } from '@angular/core';
import { NgxCaptureService } from 'ngx-capture';
import { saveAs } from 'file-saver';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  @ViewChild('screen', { static: true }) screen: any;
  imgBase64: any = '';
  constructor(private captureService: NgxCaptureService) {}

  ngOnInit(): void {}

  sayHello() {
    console.log('Hello World');
  }

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
}
