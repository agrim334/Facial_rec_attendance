<template>
  <div>
    <label for='username'> Username </label>
    <input id = 'username' type='text' placeholder ="enter name">
    <label for='pwd'> Password </label>
    <input id = 'pwd' type='password' placeholder ="enter password">
  </div>
</template>

<script>
export default {
  name: 'LogForm',
  props: {
    msg: String,
  },
};
</script>
