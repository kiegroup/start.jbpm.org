package org.jbpm.bootstrap.service.config;

import java.io.Serializable;
import java.util.Map;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties(prefix = "mapping-versions")
public class VersionMap implements Serializable {

	private static final long serialVersionUID = 147465343216850011L;
    private Map<String, String> mappedVersions;
    
    private Map<String, String> communityVersions;
    
    private Map<String, String> enterpriseVersions;
    
    
	public Map<String, String> getEnterpriseVersions() {
		return enterpriseVersions;
	}
	public void setEnterpriseVersions(Map<String, String> enterpriseVersions) {
		this.enterpriseVersions = enterpriseVersions;
	}
	public Map<String, String> getCommunityVersions() {
		return communityVersions;
	}
	public void setCommunityVersions(Map<String, String> communityVersions) {
		this.communityVersions = communityVersions;
	}
	public  Map<String, String> getMappedVersions(){
    	return mappedVersions;
    }
    public void setMappedVersions(Map<String, String> mappedVersions) {    	
    	this.mappedVersions = mappedVersions;
    	
    }    

}
