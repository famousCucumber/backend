const nodeMailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

const daemon = nodeMailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USERNAME,
        pass: process.env.EMAIL_PASSWORD
    }
});

async function sendMail(receiver, subject, html) {
    return daemon.sendMail({
        from: process.env.EMAIL_USERNAME,
        to: receiver,
        subject: subject,
        ...html && { html }
    });
}

module.exports = {
    sendMail
};
