/*
  Warnings:

  - You are about to drop the column `endTime` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `pricing` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `startTime` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `userId` on the `Conversation` table. All the data in the column will be lost.
  - The values [business_initiated,user_initiated] on the enum `Conversation_conversationType` will be removed. If these variants are still used in the database, this will fail.
  - You are about to drop the column `mediaSize` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `mediaType` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `mediaUrl` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `messageType` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `userId` on the `Message` table. All the data in the column will be lost.
  - The values [incoming,outgoing] on the enum `Message_direction` will be removed. If these variants are still used in the database, this will fail.
  - You are about to alter the column `status` on the `Message` table. The data in that column could be lost. The data in that column will be cast from `Enum(EnumId(3))` to `Enum(EnumId(5))`.
  - You are about to drop the column `languageCode` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `templateBody` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `templateName` on the `Template` table. All the data in the column will be lost.
  - You are about to alter the column `status` on the `Template` table. The data in that column could be lost. The data in that column will be cast from `Enum(EnumId(0))` to `Enum(EnumId(8))`.
  - You are about to drop the column `payload` on the `Webhook` table. All the data in the column will be lost.
  - You are about to drop the column `receivedAt` on the `Webhook` table. All the data in the column will be lost.
  - You are about to alter the column `eventType` on the `Webhook` table. The data in that column could be lost. The data in that column will be cast from `VarChar(191)` to `Enum(EnumId(11))`.
  - You are about to drop the `AuditLog` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Setting` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `User` table. If the table is not empty, all the data it contains will be lost.
  - A unique constraint covering the columns `[mediaId]` on the table `Media` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[messageId]` on the table `Message` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[name]` on the table `Template` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `phoneNumberId` to the `Conversation` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updatedAt` to the `Conversation` table without a default value. This is not possible if the table is not empty.
  - Added the required column `fileName` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `mediaId` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `phoneNumberId` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `size` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `status` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `type` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updatedAt` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `url` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `messageId` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `recipientPhoneNumberId` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `senderPhoneNumberId` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `type` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `category` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `content` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `language` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `name` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `callbackUrl` to the `Webhook` table without a default value. This is not possible if the table is not empty.
  - Added the required column `status` to the `Webhook` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updatedAt` to the `Webhook` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE `Conversation` DROP FOREIGN KEY `Conversation_userId_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_userId_fkey`;

-- DropIndex
DROP INDEX `Conversation_userId_fkey` ON `Conversation`;

-- DropIndex
DROP INDEX `Message_userId_fkey` ON `Message`;

-- AlterTable
ALTER TABLE `Conversation` DROP COLUMN `endTime`,
    DROP COLUMN `pricing`,
    DROP COLUMN `startTime`,
    DROP COLUMN `userId`,
    ADD COLUMN `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `phoneNumberId` INTEGER NOT NULL,
    ADD COLUMN `updatedAt` DATETIME(3) NOT NULL,
    MODIFY `conversationType` ENUM('INCOMING', 'OUTGOING') NOT NULL;

-- AlterTable
ALTER TABLE `Media` DROP COLUMN `mediaSize`,
    DROP COLUMN `mediaType`,
    DROP COLUMN `mediaUrl`,
    ADD COLUMN `fileName` VARCHAR(191) NOT NULL,
    ADD COLUMN `mediaId` VARCHAR(191) NOT NULL,
    ADD COLUMN `phoneNumberId` INTEGER NOT NULL,
    ADD COLUMN `size` INTEGER NOT NULL,
    ADD COLUMN `status` ENUM('SENT', 'DELIVERED', 'READ', 'FAILED') NOT NULL,
    ADD COLUMN `type` ENUM('IMAGE', 'VIDEO', 'AUDIO', 'DOCUMENT', 'STICKER') NOT NULL,
    ADD COLUMN `updatedAt` DATETIME(3) NOT NULL,
    ADD COLUMN `url` VARCHAR(191) NOT NULL;

-- AlterTable
ALTER TABLE `Message` DROP COLUMN `messageType`,
    DROP COLUMN `userId`,
    ADD COLUMN `messageId` VARCHAR(191) NOT NULL,
    ADD COLUMN `recipientPhoneNumberId` INTEGER NOT NULL,
    ADD COLUMN `senderPhoneNumberId` INTEGER NOT NULL,
    ADD COLUMN `type` ENUM('TEXT', 'IMAGE', 'VIDEO', 'AUDIO', 'DOCUMENT', 'LOCATION', 'CONTACT', 'STICKER', 'TEMPLATE', 'PRODUCT') NOT NULL,
    MODIFY `direction` ENUM('INCOMING', 'OUTGOING') NOT NULL,
    MODIFY `status` ENUM('SENT', 'DELIVERED', 'READ', 'FAILED') NOT NULL;

-- AlterTable
ALTER TABLE `Template` DROP COLUMN `languageCode`,
    DROP COLUMN `templateBody`,
    DROP COLUMN `templateName`,
    ADD COLUMN `category` ENUM('ACCOUNT_UPDATE', 'PAYMENT_UPDATE', 'SHIPPING_UPDATE', 'RESERVATION_UPDATE', 'ISSUE_RESOLUTION', 'TRANSACTIONAL', 'MARKETING', 'SOCIAL', 'OTP') NOT NULL,
    ADD COLUMN `content` VARCHAR(191) NOT NULL,
    ADD COLUMN `language` ENUM('ENGLISH', 'SPANISH', 'FRENCH', 'GERMAN', 'ITALIAN', 'PORTUGUESE', 'DUTCH', 'ARABIC', 'HINDI') NOT NULL,
    ADD COLUMN `name` VARCHAR(191) NOT NULL,
    MODIFY `status` ENUM('DRAFT', 'APPROVED', 'REJECTED', 'PENDING_APPROVAL') NOT NULL;

-- AlterTable
ALTER TABLE `Webhook` DROP COLUMN `payload`,
    DROP COLUMN `receivedAt`,
    ADD COLUMN `callbackUrl` VARCHAR(191) NOT NULL,
    ADD COLUMN `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `status` VARCHAR(191) NOT NULL,
    ADD COLUMN `updatedAt` DATETIME(3) NOT NULL,
    MODIFY `eventType` ENUM('MESSAGE_RECEIVED', 'MESSAGE_STATUS', 'DELIVERY_REPORT', 'TEMPLATE_MESSAGE', 'ERROR', 'CONTACT_UPDATED') NOT NULL;

-- DropTable
DROP TABLE `AuditLog`;

-- DropTable
DROP TABLE `Setting`;

-- DropTable
DROP TABLE `User`;

-- CreateTable
CREATE TABLE `PhoneNumber` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `phoneNumber` VARCHAR(191) NOT NULL,
    `status` ENUM('REGISTERED', 'UNREGISTERED', 'BLOCKED', 'PENDING') NOT NULL,
    `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updatedAt` DATETIME(3) NOT NULL,
    `twoStepVerificationStatus` ENUM('ENABLED', 'DISABLED') NOT NULL,

    UNIQUE INDEX `PhoneNumber_phoneNumber_key`(`phoneNumber`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Group` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `groupId` VARCHAR(191) NOT NULL,
    `name` VARCHAR(191) NOT NULL,
    `description` VARCHAR(191) NULL,
    `createdBy` INTEGER NOT NULL,
    `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updatedAt` DATETIME(3) NOT NULL,

    UNIQUE INDEX `Group_groupId_key`(`groupId`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `GroupParticipant` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `groupId` INTEGER NOT NULL,
    `participantId` INTEGER NOT NULL,
    `role` ENUM('ADMIN', 'MEMBER') NOT NULL,
    `joinedAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `ApplicationHealth` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `status` ENUM('HEALTHY', 'UNHEALTHY', 'MAINTENANCE') NOT NULL,
    `checkedAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Contact` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `phoneNumberId` INTEGER NOT NULL,
    `registered` BOOLEAN NOT NULL,
    `updatedAt` DATETIME(3) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Pricing` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `country` ENUM('IN', 'US', 'GB', 'CA', 'AU', 'DE', 'FR', 'BR', 'ZA', 'PH') NOT NULL,
    `conversationPrice` DOUBLE NOT NULL,
    `messagePrice` DOUBLE NOT NULL,
    `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `TwoStepVerification` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `phoneNumberId` INTEGER NOT NULL,
    `status` ENUM('ENABLED', 'DISABLED') NOT NULL,
    `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateIndex
CREATE UNIQUE INDEX `Media_mediaId_key` ON `Media`(`mediaId`);

-- CreateIndex
CREATE UNIQUE INDEX `Message_messageId_key` ON `Message`(`messageId`);

-- CreateIndex
CREATE UNIQUE INDEX `Template_name_key` ON `Template`(`name`);

-- AddForeignKey
ALTER TABLE `Media` ADD CONSTRAINT `Media_phoneNumberId_fkey` FOREIGN KEY (`phoneNumberId`) REFERENCES `PhoneNumber`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_senderPhoneNumberId_fkey` FOREIGN KEY (`senderPhoneNumberId`) REFERENCES `PhoneNumber`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_recipientPhoneNumberId_fkey` FOREIGN KEY (`recipientPhoneNumberId`) REFERENCES `PhoneNumber`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Group` ADD CONSTRAINT `Group_createdBy_fkey` FOREIGN KEY (`createdBy`) REFERENCES `PhoneNumber`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `GroupParticipant` ADD CONSTRAINT `GroupParticipant_groupId_fkey` FOREIGN KEY (`groupId`) REFERENCES `Group`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `GroupParticipant` ADD CONSTRAINT `GroupParticipant_participantId_fkey` FOREIGN KEY (`participantId`) REFERENCES `PhoneNumber`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Conversation` ADD CONSTRAINT `Conversation_phoneNumberId_fkey` FOREIGN KEY (`phoneNumberId`) REFERENCES `PhoneNumber`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Contact` ADD CONSTRAINT `Contact_phoneNumberId_fkey` FOREIGN KEY (`phoneNumberId`) REFERENCES `PhoneNumber`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `TwoStepVerification` ADD CONSTRAINT `TwoStepVerification_phoneNumberId_fkey` FOREIGN KEY (`phoneNumberId`) REFERENCES `PhoneNumber`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
