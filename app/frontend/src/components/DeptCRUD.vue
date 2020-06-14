<template>
 <div>
  <label for='username'> Username </label>
  <input id = 'username' type='text' placeholder ="enter name" v-model = 'user'>
  <br>
  <label for='pwd'> Password </label>
  <input id = 'pwd' type='password' placeholder ="enter password" v-model = 'pass'>
  <br>
  <label for='rembme'> Remember me? </label>
  <input id = 'rembme' type='checkbox' v-model = 'rem'>
  <br>
  <input id = 'submit' type = 'submit' placeholder ='Login'>
  <div v-if="rem == true">
    <p>{{user}}</p>
   </div>
 </div>
</template>

<script>
export default {
  name: 'EditUser',
  data() {
    return { user: '', pass: '', rem: false };
  },
};
</script>
