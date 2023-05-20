import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ZoomComponent } from './zoom/zoom.component';
import { HomeComponent } from './home/home.component';
const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'meeting', component: ZoomComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
