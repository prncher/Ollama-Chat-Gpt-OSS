import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  chats:number[] = []
  getTitle() {
    return "Add a new chat window by clicking the button"
  }

  addChat(){
    if (this.chats.length < 3){
      this.chats.push(this.chats.length+1)
    }
  }

  canAddChat(){
    return this.chats.length >= 3
  }
}
