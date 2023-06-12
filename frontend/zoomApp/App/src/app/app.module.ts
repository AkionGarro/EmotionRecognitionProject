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
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { PruebaComponent } from './prueba/prueba.component';
import { GraficosComponent } from './graficos/graficos.component';
import { NgChartsModule } from 'ng2-charts';
@NgModule({
  declarations: [
    AppComponent,
    ZoomComponent,
    NavigationComponent,
    HomeComponent,
    AboutComponent,
    PruebaComponent,
    GraficosComponent,
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
    HttpClientModule,NgChartsModule
    
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
