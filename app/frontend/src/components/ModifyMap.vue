<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>Map ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'modmap.cid' value = 'maprec.cid' />
    <br>

    <label>Map name</label>
    <input type="text" placeholder = "Enter UID" v-model = 'modmap.uid' value = 'maprec.uid'/>
    <br>

    <label>Map name</label>
    <input type="text" placeholder = "Enter User Role"
    v-model = 'modmap.role' value = 'maprec.role' />
    <br>

    <input type="submit" value="Modify map" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'ModifyMapForm',
  props: { maprec: Array },
  data() {
    return {
      modmap: {
        cid: '', uid: '', role: '',
      },
    };
  },
  methods: {
    handle() {
      this.$emit('mapupd', this.modmap);
    },
  },
};
</script>
