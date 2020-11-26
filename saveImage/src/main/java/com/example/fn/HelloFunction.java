package com.example.fn;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.oracle.bmc.ConfigFileReader;
import com.oracle.bmc.Region;
import com.oracle.bmc.auth.ConfigFileAuthenticationDetailsProvider;
import com.oracle.bmc.objectstorage.ObjectStorage;
import com.oracle.bmc.objectstorage.ObjectStorageClient;
import com.oracle.bmc.objectstorage.requests.PutObjectRequest;
import com.oracle.bmc.objectstorage.responses.PutObjectResponse;

public class HelloFunction {

	private static final Logger logger = LoggerFactory.getLogger(HelloFunction.class);
	private String configurationFilePath = "./oci/config";
	private Region region = Region.AP_SEOUL_1;
	private ObjectStorage objStoreClient;

	public HelloFunction() {
		try {
			ConfigFileReader.ConfigFile configFile = ConfigFileReader.parse(configurationFilePath);
			ConfigFileAuthenticationDetailsProvider provider = new ConfigFileAuthenticationDetailsProvider(configFile);
			objStoreClient = new ObjectStorageClient(provider);
			objStoreClient.setRegion(region);
		} catch (Exception e) {
			e.printStackTrace();
			throw new RuntimeException(e.getMessage(), e);
		}

	}

	public static class ObjectInfo {

		private String name;
		private String bucketName;
		private String content;

		public String getBucketName() {
			return bucketName;
		}

		public void setBucketName(String bucketName) {
			this.bucketName = bucketName;
		}

		public ObjectInfo() {
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

		public String getContent() {
			return content;
		}

		public void setContent(String content) {
			this.content = content;
		}

		@Override
		public String toString() {
			return "ObjectInfo [name=" + name + ", bucketName=" + bucketName + ", content=" + content + "]";
		}
	}

	public String handleRequest(ObjectInfo objectInfo) {
		// String name = (input == null || input.isEmpty()) ? "world" : input;
		logger.info("objectInfo = " + objectInfo);
		String name = "world";

		String result = "Fail";

		if (objectInfo != null) {
			logger.info("getName = " + objectInfo.getName());
			logger.info("getBucketName = " + objectInfo.getBucketName());
			logger.info("getContent = " + objectInfo.getContent());
		}

		if (objStoreClient == null) {
			System.err.println("There was a problem creating the ObjectStorage Client object. Please check logs");
			return result;
		}

		try {
			String nameSpace = "cnkkizq5yyiz";
			PutObjectRequest por = PutObjectRequest.builder().namespaceName(nameSpace).bucketName(objectInfo.bucketName)
					.objectName(objectInfo.name)
					.putObjectBody(new ByteArrayInputStream(objectInfo.content.getBytes(StandardCharsets.UTF_8)))
					.build();

			PutObjectResponse poResp = objStoreClient.putObject(por);
			result = "Successfully submitted Put request for object " + objectInfo.name + " in bucket "
					+ objectInfo.bucketName + ". OPC reuquest ID is " + poResp.getOpcRequestId();
			System.err.println(result);

		} catch (Throwable e) {
			System.err.println("Error storing object in bucket " + e.getMessage());
			result = "Error storing object in bucket " + e.getMessage();
		}

		System.out.println("Inside Java Hello World function");
		return "Hello, " + name;
	}

}
