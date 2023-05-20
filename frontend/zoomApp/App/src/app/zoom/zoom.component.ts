import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-zoom',
  templateUrl: './zoom.component.html',
  styleUrls: ['./zoom.component.css'],
})
export class ZoomComponent implements OnInit {
  meetingId: string = '';
  password: string = '';
  ngOnInit(): void {}

  async onJoinClick() {
    this.joinMeeting(this.meetingId, this.password);
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
}
