import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-zoom',
  templateUrl: './zoom.component.html',
  styleUrls: ['./zoom.component.css'],
})
export class ZoomComponent implements OnInit {
  constructor() {}
  ngOnInit(): void {}

  async ngAfterContentInit(): Promise<any> {
    const { ZoomMtg } = await import('@zoomus/websdk');
    ZoomMtg.setZoomJSLib('https://source.zoom.us/lib', '/av');
    ZoomMtg.prepareWebSDK();

    let payload = {
      meetingNumber: '',
      passWord: '',
      sdkKey: '',
      sdkSecret: '',
      userName: 'Akion',
      userEmail: '',
      role: '0',
      leaveUrl: 'http://localhost:4200',
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
              sdkKey: payload.sdkKey,
              userName: payload.userName,
              userEmail: payload.userEmail,
              signature: signature.result,
              tk: '',
              success: function (data: any) {
                console.log('join meeting success');
              },
              error: function (error: any) {
                console.log('Error Join', error);
              },
            });
          },
          error: function (error: any) {
            console.log('Error INit', error);
          },
        });
      },
      error: function (error: any) {
        console.log(error);
      },
    });
  }
}
