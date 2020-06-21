<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>User ID</label>
    <input type="text" placeholder = "Enter UID" v-model = 'attdrec.userid' value = 'user' />
    <br>

    <label>Course ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'attdrec.courseid' />
    <br>

    <label> Class Image </label>
    <input type="file" accept="image/*" id="file-input">
    <br>

    <input type="submit" value="Mark Attendance" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'MarkAttdFaceForm',
  props: { user: String },
  data() {
    return {
      attdrec: {
        userid: '', courseid: '',
      },
    };
  },
  methods: {
    handle() {
      this.$emit('attdmark', this.attdrec);
    },
  },
};
</script>
