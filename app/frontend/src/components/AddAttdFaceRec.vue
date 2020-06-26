<template>
  <div id="register-form">
    <form @submit.prevent="validate">
    <label>User ID</label>
    <input type="text" placeholder = "Enter UID" v-model = 'attdrec.uid' />
    <br>

    <label>Course ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'attdrec.cid' />
    <br>

    <label> Class Image </label>
    <input type="file" id="files" ref="files" accept="image/*" multiple />
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
        uid: '',
        cid: '',
      },
      files: '',
    };
  },
  methods: {
    validate() {
      let f = 0;
      if (this.attdrec.uid === null || this.attdrec.uid === '') {
        alert('enter uid');
        f = 1;
      }
      if (this.attdrec.cid === null || this.attdrec.cid === '') {
        alert('enter cid');
        f = 1;
      }
      this.files = this.$refs.files.files;
      console.log('efew');
      if (f === 0) {
        this.$emit('attdmark', { rec: this.attdrec, img: this.files });
      }
    },
  },
};
</script>
