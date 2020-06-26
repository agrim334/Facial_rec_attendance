<template>
  <div id="modify-form">
    <form @submit.prevent="validate">
    <label>Prof/TA ID</label>
    <input type="text" placeholder = "Enter New MarkerID" v-model = 'modattd.markerid'
    value = 'attdrec.markerid' />
    <br>

    <label>Student ID</label>
    <input type="text" placeholder = "Enter New Student ID" v-model = 'modattd.markeeid'
    value = 'attdrec.markeeid'/>
    <br>

    <label>Course ID</label>
    <input type="text" placeholder = "Enter new Course ID" v-model = 'modattd.cid'
    value = 'attdrec.cid'/>
    <br>

    <label>TimeStamp(Date of class) </label>
    <input type="text" placeholder = "Enter new Timestamp" v-model = 'modattd.ts'
    value = 'attdrec.email'/>
    <br>

    <input type="submit" value="Modify attd" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'ModifyAttdForm',
  props: { attdrec: Array },
  data() {
    return {
      modattd: {
        markerid: this.attdrec.markerid,
        markeeid: this.attdrec.markeeid,
        cid: this.attdrec.cid,
        ts: this.attdrec.ts,
      },
    };
  },
  methods: {
    validate() {
      let f = 0;
      if (this.modattd.markerid === null || this.modattd.markerid === '') {
        f = 1;
      }
      if (this.modattd.markeeid === null || this.modattd.markeeid === '') {
        f = 1;
      }
      if (this.modattd.cid === null || this.modattd.cid === '') {
        f = 1;
      }
      if (this.modattd.ts === null || this.modattd.ts === '') {
        f = 1;
      }
      if (f === 0) {
        this.$emit('attdupd', this.modattd);
      }
    },
  },
};
</script>
