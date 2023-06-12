import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ZoomComponent } from './zoom/zoom.component';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { PruebaComponent } from './prueba/prueba.component';
import { GraficosComponent } from './graficos/graficos.component';
const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'meeting', component: ZoomComponent },
  { path: 'about', component: AboutComponent },
  { path: 'prueba', component: PruebaComponent },
  { path: 'charts', component: GraficosComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
