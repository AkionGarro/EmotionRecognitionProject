import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ZoomComponent } from './zoom/zoom.component';

@NgModule({
  declarations: [AppComponent, ZoomComponent],
  imports: [
    BrowserModule,
    RouterModule.forRoot([
      {
        path: 'meeting',
        component: ZoomComponent,
      },
    ]),
    AppRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
