"use strict";(self.webpackChunkapp=self.webpackChunkapp||[]).push([[9944],{9944:(C,p,a)=>{a.r(p),a.d(p,{RegisterPageModule:()=>Z});var u=a(6814),i=a(1929),c=a(95),d=a(1837),e=a(9212),h=a(3076);function m(r,o){if(1&r&&(e.TgZ(0,"h2",10),e._uU(1),e.qZA()),2&r){const t=e.oxw();e.xp6(1),e.Oqu(t.error)}}function _(r,o){if(1&r&&(e.TgZ(0,"ion-text",10),e._uU(1),e.qZA()),2&r){const t=e.oxw();e.xp6(1),e.hij(" ",t.username_error," ")}}function f(r,o){if(1&r&&(e.TgZ(0,"ion-text",10),e._uU(1),e.qZA()),2&r){const t=e.oxw();e.xp6(1),e.hij(" ",t.email_error," ")}}function P(r,o){if(1&r&&(e.TgZ(0,"ion-text",10),e._uU(1),e.qZA()),2&r){const t=e.oxw();e.xp6(1),e.hij(" ",t.password_error," ")}}function w(r,o){if(1&r&&(e.TgZ(0,"ion-text",10),e._uU(1),e.qZA()),2&r){const t=e.oxw();e.xp6(1),e.hij(" ",t.reTypePassword_error," ")}}const M=[{path:"",component:(()=>{var r;class o{ngOnInit(){localStorage.getItem("voiceGptAccessToken")&&this.router.navigate(["/home"])}constructor(s,n){this.userService=s,this.router=n,this.username="",this.email="",this.password="",this.reTypePassword="",this.error="",this.username_error="",this.email_error="",this.password_error="",this.reTypePassword_error=""}resetErrors(){this.error="",this.username_error="",this.email_error="",this.password_error="",this.reTypePassword_error=""}onRegisterClick(){this.resetErrors(),this.username||this.email||this.password?this.username?this.email?this.password?this.password.length<6?this.password_error="Password must be at least 6 characters long.":this.password!==this.reTypePassword?this.password_error="Password is not the same":this.registerUser():this.password_error="Password is required.":this.email_error="Email is required.":this.username_error="Username is required":this.error="All fields are required!"}registerUser(){this.userService.register(this.username,this.email,this.password).subscribe({next:s=>{this.username="",this.email="",this.password="",this.router.navigate(["/login"])},error:s=>{this.error=s.error.message}})}}return(r=o).\u0275fac=function(s){return new(s||r)(e.Y36(h.K),e.Y36(d.F0))},r.\u0275cmp=e.Xpm({type:r,selectors:[["app-register"]],decls:27,vars:10,consts:[["id","my-body",3,"fullscreen"],["id","container"],["src","../../assets/icon/logo.png"],["color","danger",4,"ngIf"],["label","Username","placeholder","Select a unique Username","type","text",3,"ngModel","ngModelChange"],["label","Email","placeholder","Enter email","type","email",3,"ngModel","ngModelChange"],["label","Password","placeholder","Enter password","type","password",3,"ngModel","ngModelChange"],["label","Confirm Password","placeholder","Retype password","type","password",3,"ngModel","ngModelChange"],["expand","full","color","primary",3,"click"],["href","/login"],["color","danger"]],template:function(s,n){1&s&&(e.TgZ(0,"ion-content",0)(1,"div",1)(2,"ion-row")(3,"ion-col"),e._UZ(4,"img",2),e.qZA()(),e.TgZ(5,"ion-row")(6,"ion-col"),e.YNc(7,m,2,1,"h2",3),e.qZA()(),e.TgZ(8,"ion-list")(9,"ion-item")(10,"ion-input",4),e.NdJ("ngModelChange",function(g){return n.username=g}),e.qZA(),e.YNc(11,_,2,1,"ion-text",3),e.qZA(),e.TgZ(12,"ion-item")(13,"ion-input",5),e.NdJ("ngModelChange",function(g){return n.email=g}),e.qZA(),e.YNc(14,f,2,1,"ion-text",3),e.qZA(),e.TgZ(15,"ion-item")(16,"ion-input",6),e.NdJ("ngModelChange",function(g){return n.password=g}),e.qZA(),e.YNc(17,P,2,1,"ion-text",3),e.qZA(),e.TgZ(18,"ion-item")(19,"ion-input",7),e.NdJ("ngModelChange",function(g){return n.reTypePassword=g}),e.qZA(),e.YNc(20,w,2,1,"ion-text",3),e.qZA()(),e.TgZ(21,"ion-button",8),e.NdJ("click",function(){return n.onRegisterClick()}),e._uU(22,"Signup"),e.qZA(),e.TgZ(23,"h4"),e._uU(24,"Already have an account? "),e.TgZ(25,"a",9),e._uU(26,"Login"),e.qZA()()()()),2&s&&(e.Q6J("fullscreen",!0),e.xp6(7),e.Q6J("ngIf",n.error),e.xp6(3),e.Q6J("ngModel",n.username),e.xp6(1),e.Q6J("ngIf",n.username_error),e.xp6(2),e.Q6J("ngModel",n.email),e.xp6(1),e.Q6J("ngIf",n.email_error),e.xp6(2),e.Q6J("ngModel",n.password),e.xp6(1),e.Q6J("ngIf",n.password_error),e.xp6(2),e.Q6J("ngModel",n.reTypePassword),e.xp6(1),e.Q6J("ngIf",n.reTypePassword_error))},dependencies:[u.O5,c.JJ,c.On,i.YG,i.wI,i.W2,i.pK,i.Ie,i.q_,i.Nd,i.yW,i.j9],styles:["ion-content[_ngcontent-%COMP%]{--background: #20493c}ion-input[_ngcontent-%COMP%], ion-list[_ngcontent-%COMP%], ion-item[_ngcontent-%COMP%]{--background: transparent;background-color:transparent}#logo[_ngcontent-%COMP%]{background-color:#20493c}#container[_ngcontent-%COMP%]{width:50%;margin-left:auto;margin-right:auto;text-align:center;position:absolute;left:0;right:0;top:50%;transform:translateY(-50%)}#container[_ngcontent-%COMP%]   strong[_ngcontent-%COMP%]{font-size:20px;line-height:26px}#container[_ngcontent-%COMP%]   p[_ngcontent-%COMP%]{font-size:16px;line-height:22px;color:#8c8c8c;margin:0}#container[_ngcontent-%COMP%]   a[_ngcontent-%COMP%]{text-decoration:none}@media only screen and (max-width: 767px){#container[_ngcontent-%COMP%]{width:100%}}"]}),o})()}];let x=(()=>{var r;class o{}return(r=o).\u0275fac=function(s){return new(s||r)},r.\u0275mod=e.oAB({type:r}),r.\u0275inj=e.cJS({imports:[d.Bz.forChild(M),d.Bz]}),o})();var T=a(9862);let Z=(()=>{var r;class o{}return(r=o).\u0275fac=function(s){return new(s||r)},r.\u0275mod=e.oAB({type:r}),r.\u0275inj=e.cJS({imports:[u.ez,c.u5,i.Pc,x,T.JF]}),o})()}}]);