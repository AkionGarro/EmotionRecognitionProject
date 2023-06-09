import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ZoomComponent } from './zoom/zoom.component';
import { NavigationComponent } from './navigation/navigation.component';
import { HomeComponent } from './home/home.component';
import { FormsModule } from '@angular/forms';
import { AboutComponent } from './about/about.component';
import { NgxCaptureModule } from 'ngx-capture';
@NgModule({
  declarations: [
    AppComponent,
    ZoomComponent,
    NavigationComponent,
    HomeComponent,
    AboutComponent,
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot([
      {
        path: 'meeting',
        component: ZoomComponent,
      },
    ]),
    AppRoutingModule,
    FormsModule,
    NgxCaptureModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
